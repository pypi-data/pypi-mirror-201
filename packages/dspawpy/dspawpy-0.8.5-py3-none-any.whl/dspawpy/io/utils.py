from scipy import integrate
import re
from typing import List
import numpy as np
import os


def d_band(spin, dos_data):  # 定义函数，括号里给出函数的两个变量
    """计算d带中心

    Parameters
    ----------
    spin : Spin.up或Spin.down
        自旋类型，
    dos_data : pymatgen.electronic_structure.dos.CompleteDos
        dos数据

    Returns
    -------
    db1 : float
        d带中心数值

    Examples
    --------
    >>> from dspawpy.io.utils import d_band
    >>> from dspawpy.io.read import get_dos_data
    >>> dd = get_dos_data("dos.h5")  # 从dos.h5中读取数据
    >>> db1 = d_band(spin=Spin.up, dos_data=dd)
    >>> print(db1)
    """

    dos_d = dos_data.get_spd_dos()[2]
    Efermi = dos_data.efermi
    epsilon = dos_d.energies - Efermi  # shift d-band center

    N1 = dos_d.densities[spin]
    M1 = epsilon * N1
    SummaM1 = integrate.simps(M1, epsilon)
    SummaN1 = integrate.simps(N1, epsilon)

    return SummaM1 / SummaN1


def get_ele_from_h5(hpath: str = "aimd.h5"):
    """从h5文件中读取元素列表

    Parameters
    ----------
    hpath : str
        h5文件路径

    Returns
    -------
    ele : list
        元素列表, Natom x 1

    Examples
    --------
    >>> from dspawpy.io.utils import get_ele_from_h5
    >>> ele = get_ele_from_h5(hpath='aimd.h5')
    ['H', 'H', 'O']
    """
    import h5py

    data = h5py.File(hpath)
    Elements_bytes = np.array(data.get("/AtomInfo/Elements"))
    tempdata = np.array([i.decode() for i in Elements_bytes])
    ele = "".join(tempdata).split(";")

    return ele


def get_pos_ele_lat(spath: str):
    """从DSPAW的as结构文件中读取坐标、元素列表，和晶胞信息

    Parameters
    ----------
    path : str
        结构文件路径

    Returns
    -------
    pos : np.ndarray
        坐标分量数组，Natom x 3
    ele : list
        元素列表, Natom x 1
    latv : np.ndarray
        晶胞矢量数组，3 x 3

    Examples
    --------
    >>> from dspawpy.io.utils import get_pos_ele_lat
    >>> pos, ele, latv = get_pos_ele_lat(spath='structure.as')
    >>> pos
    array([[ 0.        ,  0.        ,  9.06355632],
           [ 1.59203323,  0.91916082, 10.62711265],
           [ 1.59203323,  0.91916082,  7.5       ]])
    >>> ele
    ['Mo', 'S', 'S']
    >>> latv
    array([[ 3.18406646,  0.        ,  0.        ],
           [-1.59203323,  2.75748245,  0.        ],
           [ 0.        ,  0.        , 30.        ]])
    """

    with open(spath, "r") as f:
        lines = f.readlines()
        Natom = int(lines[1])  # 原子总数
        ele = [line.split()[0] for line in lines[7 : 7 + Natom]]  # 元素列表

        # 晶格矢量
        latv = np.array([line.split()[0:3] for line in lines[3:6]], dtype=float)
        # xyz坐标分量
        coord = np.array(
            [line.split()[1:4] for line in lines[7 : 7 + Natom]], dtype=float
        )
        if lines[6].startswith("C"):
            pos = coord
        elif lines[6].startswith("D"):  # 分数 --> 笛卡尔
            pos = np.dot(coord, latv)
        else:
            raise ValueError(f"{spath}中的坐标类型未知！")

    return pos, ele, latv


def get_spo_ele_lat(spath: str):
    """从DSPAW的as结构文件中读取分数坐标、元素列表，和晶胞信息

    Parameters
    ----------
    spath : str
        结构文件路径

    Returns
    -------
    spos : np.ndarray
        分数坐标分量数组，Natom x 3
    ele : list
        元素列表, Natom x 1
    latv : np.ndarray
        晶胞矢量数组，3 x 3

    Examples
    --------
    >>> from dspawpy.io.utils import get_spo_ele_lat
    >>> spos, ele, latv = get_spo_ele_lat(spath='structure.as')
    >>> spos
    array([[0.        , 0.        , 0.30211854],
           [0.66666667, 0.33333333, 0.35423709],
           [0.66666667, 0.33333333, 0.25      ]])
    >>> ele
    ['Mo', 'S', 'S']
    >>> latv
    array([[ 3.18406646,  0.        ,  0.        ],
           [-1.59203323,  2.75748245,  0.        ],
           [ 0.        ,  0.        , 30.        ]])
    """

    with open(spath, "r") as f:
        lines = f.readlines()
        Natom = int(lines[1])  # 原子总数
        ele = [line.split()[0] for line in lines[7 : 7 + Natom]]  # 元素列表

        # 晶格矢量
        latv = np.array([line.split() for line in lines[3:6]], dtype=float)
        # xyz坐标分量
        coord = np.array(
            [line.split()[1:4] for line in lines[7 : 7 + Natom]], dtype=float
        )
        if lines[6].startswith("C"):  # 笛卡尔 --> 分数坐标
            spos = np.linalg.solve(latv.T, np.transpose(coord)).T
        elif lines[6].startswith("D"):
            spos = coord
        else:
            raise ValueError(f"{spath}中的坐标类型未知！")

    return spos, ele, latv


def thermo_correction(fretxt: str = "frequency.txt", T: float = 298.15):
    """从fretext中读取数据，计算ZPE和TS

    将另外保存结果到 ZPE_TS.dat 中

    Parameters
    ----------
    fretxt : str
        记录频率信息的文件所在路径, 默认当前路径下的'frequency.txt'
    T : float
        温度，单位K, 默认298.15

    Returns
    -------
    ZPE: float
        零点能
    TS: float
        熵校正

    Examples
    --------
    >>> from dspawpy.io.utils import thermo_correction
    >>> ZPE, TS = thermo_correction(fretxt='frequency.txt', T=298.15)
    >>> ZPE
    0.8842567390000002
    >>> TS
    0.18362317157111566
    """

    # 1. read data
    data_get_ZPE = []
    data_get_TS = []

    with open(fretxt, "r") as f:
        for line in f.readlines():
            data_line = line.strip().split()
            if len(data_line) != 6:
                continue
            if data_line[1] == "f":
                data_get_ZPE.append(float(data_line[5]))
                data_get_TS.append(float(data_line[2]))

    data_get_ZPE = np.array(data_get_ZPE)
    data_get_TS = np.array(data_get_TS)

    # 2. printout to check
    print(f"=== 从{fretxt}中读取到的相关如下 ===")
    print("    ZPE(meV) \t TS(THz)：")
    for i in range(len(data_get_ZPE)):
        print(" ", data_get_ZPE[i], "\t", data_get_TS[i])
    print("-" * 40)

    if len(data_get_ZPE) == 0:
        raise ValueError("全是虚频，请考虑重新优化结构...")
    else:
        print("正在写入ZPE_TS.dat文件...")
        np.savetxt(
            "ZPE_TS.dat",
            np.array([data_get_ZPE, data_get_TS]).T,
            fmt="%.6f",
            header="ZPE(meV) \t TS(THz)",
            comments=f"Data read from {os.path.abspath(fretxt)}\n",
        )

    # 3. calculate
    ZPE = 0
    for data in data_get_ZPE:
        ZPE += data / 2000.0
    print("\n--> 零点振动能为：", ZPE)

    # T = 298.15 #温度 单位：K
    # S = 0
    Na = 6.02214179e23  # 阿伏伽德罗常数 单位 /mol
    h = 6.6260696e-34  # 普朗克常数 单位J*s
    kB = 1.3806503e-23  # 玻尔兹曼常数 J/K
    R = Na * kB  # 理想气体常数 J/(K*mol)
    # THz = 1e+12 # 1 Hz = 1e+12 THz
    # e = 1.60217653E-19 #单位 C

    sum_S = 0
    import math  # 因为要使用 e的多少次方，ln（）对数

    for vi_THz in data_get_TS:
        vi_Hz = vi_THz * 1e12
        m1 = h * Na * vi_Hz
        m2 = h * vi_Hz / (kB * T)
        m3 = math.exp(m2) - 1
        m4 = T * m3
        m5 = 1 - math.exp(-m2)  # math.exp(3) 就是e的3次方
        m6 = math.log(m5, math.e)  # m6= ln(m5)   math.e在python中=e ，以右边为底的对数
        m7 = R * m6
        m8 = m1 / m4 - m7  # S 单位J/(mol*K)
        m9 = (T * m8 / 1000) / 96.49  # T*S,将单位化为KJ/mol, 96.49 kJ/mol = 1 eV 单位eV
        sum_S += m9

    print("--> TS为：", sum_S)

    with open("ZPE_TS.dat", "a") as f:
        f.write(f"\n--> ZPE: {ZPE}")
        f.write(f"\n--> TS: {sum_S}\n")

    return ZPE, sum_S


def get_lines_without_comment(filename: str, comment: str = "#") -> List[str]:
    lines = []
    with open(filename) as file:
        while True:
            line = file.readline()
            if line:
                line = re.sub(comment + r".*$", "", line)  # remove comment
                line = line.strip()
                if line:
                    lines.append(line)
            else:
                break

    return lines


def _get_coordinateType_from_h5(hpath: str = "aimd.h5"):
    """从h5文件中读取坐标类型

    Parameters
    ----------
    hpath : str
        h5文件路径

    Returns
    -------
    coordinateType : list
        坐标类型

    Examples
    --------
    >>> from dspawpy.io.utils import get_coordinateType_from_h5
    >>> coordinateType = get_coordinateType_from_h5(hpath='scf.h5')
    ['Cartesian']
    """
    import h5py

    data = h5py.File(hpath)
    CoordinateType = np.array(data.get("/AtomInfo/CoordinateType"))
    tempdata = np.array([i.decode() for i in CoordinateType])
    coordinateType = "".join(tempdata).split(";")[0]

    return coordinateType

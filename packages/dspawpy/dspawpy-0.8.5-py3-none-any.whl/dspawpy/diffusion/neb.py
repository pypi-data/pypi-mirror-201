# -*- coding: utf-8 -*-
import json
import os
from typing import List
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from pymatgen.core import Structure
from dspawpy.io.read import load_h5
from dspawpy.io.structure import to_file
from dspawpy.diffusion.pathfinder import IDPPSolver


class NEB:
    """

    Parameters
    ----------
    initial_structure: Structure
        初态
    final_structure: Structure
        终态
    nimages: int
        中间构型数

    Examples
    --------
    >>> from pymatgen.core import Structure
    # 先调用pymatgen写好的from_file方法读取cif构型文件，生成structure对象
    >>> initial_structure = Structure.from_file("initial.cif")
    >>> final_structure = Structure.from_file("final.cif")
    # 初始化对象，后续可以调用两个插值算法，详见下方write_neb_structures
    >>> from dspawpy.diffusion.neb import NEB
    >>> neb = NEB(initial_structure,final_structure,10)
    """

    def __init__(self, initial_structure, final_structure, nimages):
        """

        Args:
            initial_structure:
            final_structure:
            nimages: number of images,contain initial and final structure
        """

        self.nimages = nimages
        self.iddp = IDPPSolver.from_endpoints(
            endpoints=[initial_structure, final_structure], nimages=self.nimages - 2
        )

    def linear_interpolate(self):
        return self.iddp.structures

    def idpp_interpolate(
        self,
        maxiter=1000,
        tol=1e-5,
        gtol=1e-3,
        step_size=0.05,
        max_disp=0.05,
        spring_const=5.0,
    ):
        return self.iddp.run(maxiter, tol, gtol, step_size, max_disp, spring_const)


def plot_neb_barrier(
    datafile: str,
    ri: float = None,
    rf: float = None,
    ei: float = None,
    ef: float = None,
    show: bool = True,
    figname: str = "neb_reaction_coordinate.png",
):
    """根据neb.json或者neb.h5绘制能垒图

    如果NEB任务不计算初末态的自洽，这两个文件中将缺失相关信息，需要手动输入

    Parameters
    ----------
    datafile : str
        neb.json或neb.h5文件路径
    ri : float
        初态反应坐标
    rf : float
        末态反应坐标
    ei : float
        初态自洽能量
    ef : float
        末态自洽能量
    show : bool, optional
        是否展示交互式绘图窗口, 默认展示
    figname : str
        保存的图片名称, 默认'neb_reaction_coordinate.png'

    Returns
    -------
    NEB能垒图

    Examples
    --------
    >>> from dspawpy.diffusion.neb import plot_neb_barrier
    >>> plot_neb_barrier("neb.h5") # neb.iniFin = true
    >>> plot_neb_barrier("neb.h5",ri=0.0,rf=1.0,ei=-1.0,ef=-2.0) # neb.iniFin = false
    """
    # search datafile in the given directory
    if os.path.isdir(datafile):
        directory = datafile  # specified datafile is actually a directory
        print("您指定了一个文件夹，正在查找相关h5或json文件...")
        if os.path.exists(os.path.join(directory, "neb.h5")):
            datafile = os.path.join(directory, "neb.h5")
            print("Reading neb.h5...")
        elif os.path.exists(os.path.join(directory, "neb.json")):
            datafile = os.path.join(directory, "neb.json")
            print("Reading neb.json...")
        else:
            raise FileNotFoundError("未找到neb.h5/neb.json文件！")

    if datafile.endswith(".h5"):
        neb = load_h5(datafile)
        if "/BarrierInfo/ReactionCoordinate" in neb.keys():
            reaction_coordinate = neb["/BarrierInfo/ReactionCoordinate"]
            energy = neb["/BarrierInfo/TotalEnergy"]
        else:  # old version
            reaction_coordinate = neb["/Distance/ReactionCoordinate"]
            energy = neb["/Energy/TotalEnergy"]
    elif datafile.endswith(".json"):
        with open(datafile, "r") as fin:
            neb = json.load(fin)
        if "BarrierInfo" in neb.keys():
            reaction_coordinate = neb["BarrierInfo"]["ReactionCoordinate"]
            energy = neb["BarrierInfo"]["TotalEnergy"]
        else:  # old version
            reaction_coordinate = neb["Distance"]["ReactionCoordinate"]
            energy = neb["Energy"]["TotalEnergy"]
    else:
        raise TypeError("仅支持读取h5或json文件！")

    x = []
    for c in reaction_coordinate:
        if len(x) > 0:
            x.append(x[-1] + c)
        else:
            x.append(c)

    y = [x - energy[0] for x in energy]
    # initial and final info
    if ri is not None:  # add initial reaction coordinate
        x.insert(0, ri)
    if rf is not None:  # add final reaction coordinate
        x.append(rf)

    if ei is not None:  # add initial energy
        y.insert(0, ei)
    if ef is not None:  # add final energy
        y.append(ef)

    inter_f = interp1d(x, y, kind="cubic")
    xnew = np.linspace(x[0], x[-1], 100)
    ynew = inter_f(xnew)

    plt.plot(xnew, ynew, c="b")
    plt.scatter(x, y, c="r")
    plt.xlabel("Reaction Coordinate")
    plt.ylabel("Energy")

    if figname:
        plt.tight_layout()
        plt.savefig(figname)
    if show:
        plt.show()


def write_neb_structures(
    structures: List[Structure],
    coords_are_cartesian=True,
    fmt: str = "json",
    path: str = ".",
    prefix="structure",
):
    """插值并生成中间构型文件

    Parameters
    ----------
    structures: list
        构型列表
    coords_are_cartesian: bool
        坐标是否为笛卡尔坐标
    fmt: str
        结构文件类型，支持 "json", "as", "poscar", "hzw"
    path: str
        保存路径

    Returns
    -------
    file
        保存构型文件

    Examples
    --------
    >>> from pymatgen.core import Structure
    # 先调用pymatgen写好的from_file方法读取cif构型文件，生成structure对象
    >>> initial_structure = Structure.from_file("initial.cif")
    >>> final_structure = Structure.from_file("final.cif")
    # 插值并生成中间构型文件
    >>> from dspawpy.diffusion.neb import NEB,write_neb_structures
    >>> neb = NEB(initial_structure,final_structure,10)
    >>> neb = NEB(init_struct,final_struct,5) # 设置插点个数
    >>> structures = neb.idpp_interpolate() # idpp插值，生成中间构型
    # 可指定保存到neb文件夹下
    >>> write_neb_structures(structures,coords_are_cartesian=True,fmt="as",path="neb")
    """
    N = len(str(len(structures)))
    if N <= 2:
        N = 2
    for i, structure in enumerate(structures):
        path_name = str(i).zfill(N)
        os.makedirs(os.path.join(path, path_name), exist_ok=True)
        if fmt == "poscar":
            structure.to(fmt="poscar", filename=os.path.join(path, path_name, "POSCAR"))
        else:
            filename = os.path.join(
                path, path_name, "%s%s.%s" % (prefix, path_name, fmt)
            )
            to_file(
                structure, filename, coords_are_cartesian=coords_are_cartesian, fmt=fmt
            )


def plot_neb_converge(neb_dir: str, image_key="01"):
    # for compatibility
    if neb_dir.endswith(".h5"):
        neb_total = load_h5(neb_dir)
        maxforce = np.array(neb_total["/Iteration/" + image_key + "/MaxForce"])
        total_energy = np.array(neb_total["/Iteration/" + image_key + "/TotalEnergy"])
    elif neb_dir.endswith(".json"):
        with open(neb_dir, "r") as fin:
            neb_total = json.load(fin)
        try:
            neb = neb_total["LoopInfo"][image_key]
        except:
            neb = neb_total["Iteration"][image_key]
        maxforce = []
        total_energy = []
        for n in neb:
            maxforce.append(n["MaxForce"])
            total_energy.append(n["TotalEnergy"])

    elif os.path.exists(f"{neb_dir}/neb.h5"):
        neb_total = load_h5(f"{neb_dir}/neb.h5")
        maxforce = np.array(neb_total["/Iteration/" + image_key + "/MaxForce"])
        total_energy = np.array(neb_total["/Iteration/" + image_key + "/TotalEnergy"])

    elif os.path.exists(f"{neb_dir}/neb.json"):
        with open(f"{neb_dir}/neb.json", "r") as fin:
            neb_total = json.load(fin)
        try:
            neb = neb_total["LoopInfo"][image_key]
        except:
            neb = neb_total["Iteration"][image_key]
        maxforce = []
        total_energy = []
        for n in neb:
            print(n)
            maxforce.append(n["MaxForce"])
            total_energy.append(n["TotalEnergy"])

        maxforce = np.array(maxforce)
        total_energy = np.array(total_energy)

    else:
        print(f"{neb_dir}路径中找不到neb.h5或者neb.json文件")

    x = np.arange(len(maxforce))

    force = maxforce
    energy = total_energy

    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    ax1.plot(x, force, label="Max Force", c="black")
    ax1.set_xlabel("Number of ionic step")
    ax1.set_ylabel("Force")

    ax2 = ax1.twinx()
    ax2.plot(x, energy, label="Energy", c="r")
    ax2.set_xlabel("Number of ionic step")
    ax2.set_ylabel("Energy")
    ax2.ticklabel_format(useOffset=False)  # y轴坐标显示绝对值而不是相对值

    fig.legend(loc=1, bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)
    plt.tight_layout()

    return ax1, ax2

# -*- coding: utf-8 -*-
import os
import numpy as np
from typing import List, Tuple, Union
from scipy.ndimage import gaussian_filter1d
from pymatgen.core import Structure
import matplotlib.pyplot as plt


class MSD:
    # 用于实际计算均方差的类，摘自pymatgen开源项目
    def __init__(
        self,
        structures: List[Structure],
        select: Union[str, List[int]] = "all",
        msd_type="xyz",
    ):
        self.structures = structures
        self.msd_type = msd_type

        self.n_frames = len(structures)
        if select == "all":
            self.n_particles = len(structures[0])
        else:
            self.n_particles = len(select)
        self.lattice = structures[0].lattice

        self._parse_msd_type()

        self._position_array = np.zeros((self.n_frames, self.n_particles, self.dim_fac))

        if select == "all":
            for i, s in enumerate(self.structures):
                self._position_array[i, :, :] = s.frac_coords[:, self._dim]
        else:
            for i, s in enumerate(self.structures):
                self._position_array[i, :, :] = s.frac_coords[select, :][:, self._dim]

    def _parse_msd_type(self):
        r"""Sets up the desired dimensionality of the MSD."""
        keys = {
            "x": [0],
            "y": [1],
            "z": [2],
            "xy": [0, 1],
            "xz": [0, 2],
            "yz": [1, 2],
            "xyz": [0, 1, 2],
        }

        self.msd_type = self.msd_type.lower()

        try:
            self._dim = keys[self.msd_type]
        except KeyError:
            raise ValueError(
                "invalid msd_type: {} specified, please specify one of xyz, "
                "xy, xz, yz, x, y, z".format(self.msd_type)
            )

        self.dim_fac = len(self._dim)

    def run(self):
        print('Calculating MSD...')
        result = np.zeros((self.n_frames, self.n_particles))

        rd = np.zeros((self.n_frames, self.n_particles, self.dim_fac))
        for i in range(1, self.n_frames):
            disp = self._position_array[i, :, :] - self._position_array[i - 1, :, :]
            # mic by periodic boundary condition
            disp[np.abs(disp) > 0.5] = disp[np.abs(disp) > 0.5] - np.sign(
                disp[np.abs(disp) > 0.5]
            )
            disp = np.dot(disp, self.lattice.matrix)
            rd[i, :, :] = disp
        rd = np.cumsum(rd, axis=0)
        for n in range(1, self.n_frames):
            disp = rd[n:, :, :] - rd[:-n, :, :]  # [n:-n] window
            sqdist = np.square(disp).sum(axis=-1)
            result[n, :] = sqdist.mean(axis=0)

        return result.mean(axis=1)


class RDF:
    # 用于快速计算径向分布函数的类
    # Copyright (c) Materials Virtual Lab.
    # Distributed under the terms of the BSD License.
    def __init__(
        self,
        structures: Union[Structure, List[Structure]],
        rmin: float = 0.0,
        rmax: float = 10.0,
        ngrid: float = 101,
        sigma: float = 0.0,
    ):
        """This method calculates rdf on `np.linspace(rmin, rmax, ngrid)` points

        Parameter
        ---------
        structures (list of pymatgen Structures): structures to compute RDF
        rmin (float): minimal radius
        rmax (float): maximal radius
        ngrid (int): number of grid points, defaults to 101
        sigma (float): smooth parameter
        """
        if isinstance(structures, Structure):
            structures = [structures]
        self.structures = structures
        # Number of atoms in all structures should be the same
        assert len({len(i) for i in self.structures}) == 1, "不同构型的原子数不等！"
        elements = [[i.specie for i in j.sites] for j in self.structures]
        unique_elements_on_sites = [len(set(i)) == 1 for i in list(zip(*elements))]

        # For the same site index, all structures should have the same element there
        if not all(unique_elements_on_sites):
            raise RuntimeError("Elements are not the same at least for one site")

        self.rmin = rmin
        self.rmax = rmax
        self.ngrid = ngrid

        self.dr = (self.rmax - self.rmin) / (self.ngrid - 1)  # end points are on grid
        self.r = np.linspace(self.rmin, self.rmax, self.ngrid)  # type: ignore

        max_r = self.rmax + self.dr / 2.0  # add a small shell to improve robustness

        self.neighbor_lists = [i.get_neighbor_list(max_r) for i in self.structures]
        # each neighbor list is a tuple of
        # center_indices, neighbor_indices, image_vectors, distances
        (
            self.center_indices,
            self.neighbor_indices,
            self.image_vectors,
            self.distances,  # 完整的距离列表（遍历体系所有原子）
        ) = list(
            zip(*self.neighbor_lists)
        )

        elements = np.array([str(i.specie) for i in structures[0]])  # type: ignore
        self.center_elements = [elements[i] for i in self.center_indices]
        self.neighbor_elements = [elements[i] for i in self.neighbor_indices]
        self.density = [{}] * len(self.structures)

        self.natoms = [
            i.composition.to_data_dict["unit_cell_composition"]
            for i in self.structures  # 抽成单胞化学式
        ]  # {'H': 2, 'O': 1} 字典构成的列表

        for s_index, natoms in enumerate(self.natoms):  # s_index是结构序号，natoms是单胞化学式字典
            for i, j in natoms.items():  # i是元素符号，j是原子个数
                self.density[s_index][i] = (
                    j / self.structures[s_index].volume
                )  # 原子数除以体积

        self.volumes = 4.0 * np.pi * self.r**2 * self.dr  # 分母的一部分
        self.volumes[self.volumes < 1e-8] = 1e8  # avoid divide by zero
        self.n_structures = len(self.structures)
        self.sigma = np.ceil(sigma / self.dr)
        # print(elements)

    def _dist_to_counts(self, d):
        """Convert a distance array for counts in the bin

        Parameter
        ---------
            d: (1D np.array)

        Returns:
            1D array of counts in the bins centered on self.r
        """
        # print(len(d))
        # print(f'{d=}\n')
        counts = np.zeros((self.ngrid,))
        indices = np.array(
            np.floor((d - self.rmin + 0.5 * self.dr) / self.dr), dtype=int
        )  # 将找到配对的距离转换为格点序号 (向下取整)
        # print(len(indices))
        # print(f'{indices=}\n')
        # 取整操作，导致格点序号很可能重复，因此需要统计每个格点序号出现的次数并去重
        unique, val_counts = np.unique(indices, return_counts=True)
        # print(len(unique))
        # print(f'{unique=}\n')
        counts[unique] = val_counts
        # print(f'{counts=}\n')
        # raise IndexError
        return counts

    def get_rdf(
        self,
        ref_species: Union[str, List[str]],
        species: Union[str, List[str]],
        is_average=True,
    ):
        """Wrapper to get the rdf for a given species pair

        Parameter
        ---------
        ref_species (list of species or just single specie str):
            The reference species. The rdfs are calculated with these species at the center
        species (list of species or just single specie str):
            the species that we are interested in. The rdfs are calculated on these species.
        is_average (bool):
            whether to take the average over all structures

        Returns
        -------
        (x, rdf)
            x is the radial points, and rdf is the rdf value.
        """
        print('Calculating RDF...')
        all_rdfs = [
                self.get_one_rdf(ref_species, species, i)[1]
                for i in range(self.n_structures)
            ]
        if is_average:
            all_rdfs = np.mean(all_rdfs, axis=0)
        return self.r, all_rdfs

    def get_one_rdf(
        self,
        ref_species: Union[str, List[str]],
        species: Union[str, List[str]],
        index=0,
    ):
        """Get the RDF for one structure, indicated by the index of the structure
        in all structures

        Parameter
        ---------
        ref_species (list of species or just single specie str):
            the reference species. The rdfs are calculated with these species at the center
        species (list of species or just single specie str):
            the species that we are interested in. The rdfs are calculated on these species.
        index (int):
            structure index in the list

        Returns
        -------
            (x, rdf) x is the radial points, and rdf is the rdf value.
        """
        if isinstance(ref_species, str):
            ref_species = [ref_species]

        if isinstance(species, str):
            species = [species]
        # print(f'{len(self.center_elements[index])=}')
        indices = (  # 须同时满足下列条件
            (np.isin(self.center_elements[index], ref_species))
            & (np.isin(self.neighbor_elements[index], species))
            & (self.distances[index] >= self.rmin - self.dr / 2.0)
            & (self.distances[index] <= self.rmax + self.dr / 2.0)
            & (self.distances[index] > 1e-8)
        )
        # print(f'{len(indices)=}')
        # raise ValueError
        # print(f'{indices=}\n')
        density = sum(self.density[index][i] for i in species)  # 目标元素的原子数密度，单浮点数
        natoms = sum(self.natoms[index][i] for i in ref_species)  # 中心元素的原子总数，单整数
        distances = self.distances[index][indices]  # 针对每个中心原子，目标元素的距离列表
        counts = self._dist_to_counts(distances)  # 统计该距离内目标元素的原子数，列表
        rdf_temp = (
            counts / density / self.volumes / natoms
        )  # counts包含了所有中心元素(ref_species)对应的原子的信息，因此需要除以中心原子总数
        if self.sigma > 1e-8:
            rdf_temp = gaussian_filter1d(rdf_temp, self.sigma)
        return self.r, rdf_temp

    def get_coordination_number(self, ref_species, species, is_average=True):
        """returns running coordination number

        Parameter
        ---------
        ref_species (list of species or just single specie str):
            the reference species. The rdfs are calculated with these species at the center
        species (list of species or just single specie str):
            the species that we are interested in. The rdfs are calculated on these species.
        is_average (bool): whether to take structural average

        Returns
        --------
        numpy array
        """
        print('Calculating coordination number...')
        # Note: The average density from all input structures is used here.
        all_rdf = self.get_rdf(ref_species, species, is_average=False)[1]
        if isinstance(species, str):
            species = [species]
        density = [sum(i[j] for j in species) for i in self.density]
        cn = [
            np.cumsum(rdf * density[i] * 4.0 * np.pi * self.r**2 * self.dr)
            for i, rdf in enumerate(all_rdf)
        ]
        if is_average:
            cn = np.mean(cn, axis=0)
        return self.r, cn


class RMSD:
    # 用于计算均方差根（Root Mean Square Deviation）的类，摘自pymatgen开源项目
    def __init__(self, structures: List[Structure]):
        self.structures = structures

        self.n_frames = len(self.structures)
        self.n_particles = len(self.structures[0])
        self.lattice = self.structures[0].lattice

        self._position_array = np.zeros((self.n_frames, self.n_particles, 3))

        for i, s in enumerate(self.structures):
            self._position_array[i, :, :] = s.frac_coords

    def run(self, base_index=0):
        print('Calculating RMSD...')
        result = np.zeros(self.n_frames)
        rd = np.zeros((self.n_frames, self.n_particles, 3))
        for i in range(1, self.n_frames):
            disp = self._position_array[i, :, :] - self._position_array[i - 1, :, :]
            # mic by periodic boundary condition
            disp[np.abs(disp) > 0.5] = disp[np.abs(disp) > 0.5] - np.sign(
                disp[np.abs(disp) > 0.5]
            )
            disp = np.dot(disp, self.lattice.matrix)
            rd[i, :, :] = disp
        rd = np.cumsum(rd, axis=0)

        for i in range(self.n_frames):
            sqdist = np.square(rd[i] - rd[base_index]).sum(axis=-1)
            result[i] = sqdist.mean()

        return np.sqrt(result)


def build_Structures_from_datafile(datafile: Union[str, List[str]]) -> List[Structure]:
    """读取一/多个h5/json文件，返回pymatgen的Structures列表

    Parameters
    ----------
    datafile : 字符串或字符串列表
        aimd.h5/aimd.json文件或包含任意这些文件文件夹；若给定字符串列表，将依次读取数据并合并成一个Structures列表

    Returns
    -------
    List[Structure] : pymatgen structures 列表

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import build_Structures_from_datafile
    # 读取单个文件
    >>> pymatgen_Structures = build_Structures_from_datafile(datafile='aimd1.h5')
    # 给定包含aimd.h5或aimd.json文件的文件夹位置
    >>> pymatgen_Structures = build_Structures_from_datafile(datafile='my_aimd_task')
    # 当datafile为列表时，将依次读取多个文件，合并成一个Structures列表
    >>> pymatgen_Structures = build_Structures_from_datafile(datafile=['aimd1.h5','aimd2.h5'])
    """
    dfs = []
    if isinstance(datafile, list):  # 续算模式，给的是多个文件
        dfs = datafile
    else:  # 单次计算模式，处理单个文件
        if os.path.isdir(datafile):
            print(f"正在查找读取文件夹 {datafile} 中的aimd.h5或aimd.json文件...")
            if os.path.exists(os.path.join(datafile, "aimd.h5")):
                df = os.path.join(datafile, "aimd.h5")
            elif os.path.exists(os.path.join(datafile, "aimd.json")):
                df = os.path.join(datafile, "aimd.json")
            else:
                raise FileNotFoundError("不存在相应的aimd.h5或aimd.json文件！")

        if datafile.endswith(".h5") or datafile.endswith(".json"):
            df = datafile
        else:
            raise FileNotFoundError("未找到aimd.h5或aimd.json文件！")
        dfs.append(df)

    # 读取结构数据
    pymatgen_Structures = []
    for df in dfs:
        # TODO 支持选取特定帧
        structure_list = _get_structure_list(df)
        pymatgen_Structures.extend(structure_list)

    return pymatgen_Structures


def get_lagtime_msd(
    datafile: Union[str, List[str]],
    select: Union[str, List[int]] = "all",
    msd_type: str = "xyz",
    timestep: float = 1.0,
):
    """计算不同时间步长下的均方差

    Parameters
    ----------
    datafile : str or list of str
        aimd.h5或aimd.json文件或包含这两个文件之一的文件夹；
        写成列表的话将依次读取数据并合并到一起
    select : str or list of int
        原子序号列表，原子序号从0开始编号；默认为'all'，计算所有原子
        暂不支持计算多个元素的MSD
    msd_type : str
        计算MSD的类型，可选xyz,xy,xz,yz,x,y,z，默认为'xyz'，即计算所有分量
    timestep : float
        时间间隔，单位为fs，默认1.0fs

    Returns
    -------
    lagtime : np.ndarray
        时间序列
    result : np.ndarray
        均方差序列

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_lagtime_msd
    >>> lagtime, msd = get_lagtime_msd(datafile='aimd.h5', select='all', msd_type='xyz', timestep=1.0)
    >>> lagtime
    array([  0.,   1.,   2.,   3.,   4.,   5.,   6.,   7.,   8.,   9.,  10.,
            11.,  12.,  13.,  14.,  15.,  16.,  17.,  18.,  19.,  20.,  21.,
            ...,
            990., 991., 992., 993., 994., 995., 996., 997., 998., 999.])
    >>> msd
    array([   0.        ,   67.07025573,  132.46384987,  193.1025821 ,
            250.1513171 ,  301.71988034,  349.76713326,  397.42586668,
            ...,
            1092.833737  , 1067.50385434, 1009.90265319, 1206.1645769 ])
    """
    strs = build_Structures_from_datafile(datafile)

    msd = MSD(strs, select, msd_type)
    result = msd.run()

    nframes = msd.n_frames
    lagtime = np.arange(nframes) * timestep  # make the lag-time axis

    return lagtime, result


def get_lagtime_rmsd(datafile: Union[str, List[str]], timestep: float = 1.0):
    """

    Parameters
    ----------
    datafile : str or list of str
        aimd.h5或aimd.json文件或包含这两个文件之一的文件夹；
        写成列表的话将依次读取数据并合并到一起
    timestep : float
        时间步长，单位fs，默认1fs

    Returns
    -------
    lagtime : numpy.ndarray
        时间序列
    rmsd : numpy.ndarray
        均方根序列

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_lagtime_rmsd
    >>> lagtime, rmsd = get_lagtime_rmsd(datafile='aimd.h5', timestep=1.0)
    >>> lagtime
    array([  0.,   1.,   2.,   3.,   4.,   5.,   6.,   7.,   8.,   9.,  10.,
            11.,  12.,  13.,  14.,  15.,  16.,  17.,  18.,  19.,  20.,  21.,
            ...,
            990., 991., 992., 993., 994., 995., 996., 997., 998., 999.])
    >>> rmsd
    array([ 0.        , 19.61783543, 19.62557403, 19.63797614, 19.65407193,
            27.77329091, 27.7898651 , 19.72260788,  2.34196454,  2.62175006,
            ...,
            43.97237636, 39.57388473, 39.67579857, 34.61880282, 34.72988017])
    """
    strs = build_Structures_from_datafile(datafile)

    rmsd = RMSD(structures=strs)
    result = rmsd.run()

    # Plot
    nframes = rmsd.n_frames
    lagtime = np.arange(nframes) * timestep  # make the lag-time axis

    return lagtime, result


def get_rs_rdfs(
    datafile: Union[str, List[str]],
    ele1: str,
    ele2: str,
    rmin: float = 0,
    rmax: float = 10,
    ngrid: float = 101,
    sigma: float = 0,
):
    """计算rdf分布函数

    Parameters
    ----------
    datafile : str or list of str
        aimd.h5或aimd.json文件路径或包含这两个文件之一的文件夹；
        写成列表的话将依次读取数据并合并到一起
    ele1 : list
        中心元素
    ele2 : list
        相邻元素
    rmin : float
        径向分布最小值，默认为0
    rmax : float
        径向分布最大值，默认为10
    ngrid : int
        径向分布网格数，默认为101
    sigma : float
        平滑参数

    Returns
    -------
    r : numpy.ndarray
        径向分布网格点
    rdf : numpy.ndarray
        径向分布函数

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_rs_rdfs
    >>> rs, rdfs = get_rs_rdfs(datafile='aimd.h5', ele1='H', ele2='O', rmin=0, rmax=10, ngrid=101, sigma=0)
    >>> rs
    array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1. ,
            1.1,  1.2,  1.3,  1.4,  1.5,  1.6,  1.7,  1.8,  1.9,  2. ,  2.1,
            ...,
            9.9, 10. ])
    >>> rdfs
    array([0.        , 0.        , 0.        , 0.        , 0.        ,
           0.        , 0.        , 0.        , 0.        , 0.        ,
           ...,
           0.97097276])]
    """
    strs = build_Structures_from_datafile(datafile)
    # print(strs[0]) # check pbc
    # raise ValueError

    # 计算rdf并绘制主要曲线
    obj = RDF(
        structures=strs, rmin=rmin, rmax=rmax, ngrid=ngrid, sigma=sigma
    )

    rs, rdfs = obj.get_rdf(ele1, ele2)
    return rs, rdfs


def plot_msd(
    lagtime: np.ndarray,
    result: np.ndarray,
    xlim: List[float] = None,
    ylim: List[float] = None,
    figname: str = None,
    show: bool = True,
    ax=None,
    **kwargs,
):
    """AIMD任务完成后，计算均方差（MSD）

    Parameters
    ----------
    lagtime : np.ndarray
        时间序列
    result : np.ndarray
        均方差序列
    xlim : list of float
        x轴的范围，默认为None，自动设置
    ylim : list of float
        y轴的范围，默认为None，自动设置
    figname : str
        图片名称，默认为None，不保存图片
    show : bool
        是否显示图片，默认为True
    ax: matplotlib axes object
        用于将图片绘制到matplotlib的子图上
    **kwargs : dict
        其他参数，如线条宽度、颜色等，传递给plt.plot函数

    Returns
    -------
    MSD分析后的图片

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_lagtime_msd, plot_msd
    # 指定h5文件位置，用 get_lagtime_msd 函数获取数据，select 参数选择第n个原子（不是元素）
    >>> lagtime, msd = get_lagtime_msd('H2O-aimd1.h5', select=[0])
    # 用获取的数据画图并保存
    >>> plot_msd(lagtime, msd, figname='MSD.png')
    """
    if ax:
        ishow = False
        ax.plot(lagtime, result, c="black", ls="-", **kwargs)
    else:
        ishow = True
        fig, ax = plt.subplots()
        ax.plot(lagtime, result, c="black", ls="-", **kwargs)
        ax.set_xlabel("Time (fs)")
        ax.set_ylabel("MSD (Å)")

    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    if figname:
        plt.savefig(figname)
        print("MSD图片保存在", os.path.abspath(figname))
    if ishow and show:  # 画子图的话，不应每个子图都show
        plt.show()  # show会自动清空图片

    return ax


def plot_rdf(
    rs: np.ndarray,
    rdfs: np.ndarray,
    ele1: str,
    ele2: str,
    xlim: list = None,
    ylim: list = None,
    figname: str = None,
    show: bool = True,
    ax: plt.Axes = None,
    **kwargs,
):
    """AIMD计算后分析rdf并画图

    Parameters
    ----------
    rs : numpy.ndarray
        径向分布网格点
    rdfs : numpy.ndarray
        径向分布函数
    ele1 : list
        中心元素
    ele2 : list
        相邻元素
    xlim : list
        x轴范围，默认为None，即自动设置
    ylim : list
        y轴范围，默认为None，即自动设置
    figname : str
        图片名称，默认为None，即不保存图片
    show : bool
        是否显示图片，默认为True
    ax: matplotlib.axes.Axes
        画图的坐标轴，默认为None，即新建坐标轴
    **kwargs : dict
        其他参数，如线条宽度、颜色等，传递给plt.plot函数

    Returns
    -------
    rdf分析后的图片

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_rs_rdfs, plot_rdf
    # 先获取rs和rdfs数据作为xy轴数据
    >>> rs, rdfs = get_rs_rdfs(['LiO-aimd1.h5','LiO-aimd2.h5','LiO-aimd3.h5'], 'Li', 'O', rmax=6)
    # 将xy轴数据传入plot_rdf函数绘图
    >>> plot_rdf(rs, rdfs, 'Li','O', xlim=[0,6], ylim=[0,35], color='red')
    """
    if ax:
        ax.plot(
            rs,
            rdfs,
            label=r"$g_{\alpha\beta}(r)$" + f"[{ele1},{ele2}]",
            **kwargs,
        )

    else:
        fig, ax = plt.subplots()
        ax.plot(
            rs,
            rdfs,
            label=r"$g_{\alpha\beta}(r)$" + f"[{ele1},{ele2}]",
            **kwargs,
        )

        ax.set_xlabel(r"$r$" + "(Å)")
        ax.set_ylabel(r"$g(r)$")

    ax.legend()

    # 绘图细节
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    if figname:
        plt.savefig(figname)
        print(f"图片已保存到 {os.path.abspath(figname)}")
    if show:  # 画子图的话，不应每个子图都show
        plt.show()  # show会自动清空图片


def plot_rmsd(
    lagtime: np.ndarray,
    result: np.ndarray,
    xlim: list = None,
    ylim: list = None,
    figname: str = None,
    show: bool = True,
    ax=None,
    **kwargs,
):
    """AIMD计算后分析rmsd并画图

    Parameters
    ----------
    lagtime:
        时间序列
    result:
        均方根序列
    xlim : list
        x轴范围
    ylim : list
        y轴范围
    figname : str
        图片保存路径
    show : bool
        是否显示图片
    ax : matplotlib.axes._subplots.AxesSubplot
        画子图的话，传入子图对象
    **kwargs : dict
        传入plt.plot的参数

    Returns
    -------
    rmsd分析结构的图片

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_lagtime_rmsd, plot_rmsd
    # timestep 表示时间步长
    >>> lagtime, rmsd = get_lagtime_rmsd(datafile='H2O-aimd1.h5', timestep=0.1)
    # 直接保存为RMSD.png图片
    >>> plot_rmsd(lagtime, rmsd, figname='RMSD.png', show=True)
    """
    # 参数初始化
    if not ax:
        ishow = True
    else:
        ishow = False

    if ax:
        ax.plot(lagtime, result, **kwargs)
    else:
        fig, ax = plt.subplots()
        ax.plot(lagtime, result, **kwargs)
        ax.set_xlabel("Time (fs)")
        ax.set_ylabel("RMSD (Å)")

    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    if figname:
        plt.savefig(figname)
    if show and ishow:  # 画子图的话，不应每个子图都show
        plt.show()  # show会自动清空图片

    return ax


def read_h5(
    hpath: str,
    index = None,
    ele = None,
    ai = None,
    return_scaled: bool = False,
):
    """从hpath指定的路径读取h5文件中的数据

    Parameters
    ----------
    hpath: str
        h5文件路径
    index: int or list or str
        运动轨迹中的第几步，从1开始计数
        如果要切片，用字符串写法： '1, 10:20, 23'
    ele: str or list or np.array
        元素，例如 'C'，'H'，'O'，'N'
    ai: int or list or np.array
        原子序号（体系中的第几个原子，不是质子数）
        如果要切片，用字符串写法： '1, 10:20, 23'
    return_scaled: bool
        是否返回原子分数坐标，默认为False

    Return
    -------
    Nstep: int
        离子步总数
    elements: list
        元素列表, Natom x 1
    positions: np.ndarray
        原子位置,  Nstep x Natom x 3
    lattices: np.ndarray
        晶胞, Nstep x 3 x 3

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import read_h5
    >>> Nstep, elements, positions, lattices = read_h5(hpath='aimd.h5', ele='H', index='1:2')
    >>> Nstep
    2
    >>> elements
    ['H', 'H']
    >>> positions
    array([[[0.56037855, 5.60910012, 0.06341764],
            [0.57622933, 0.78033174, 6.28639689]],
           [[0.55354018, 5.60627362, 0.12845834],
            [0.57012995, 0.80246543, 6.22272366]]])
    >>> lattices
    array([[[6.35016, 0.     , 0.     ],
            [0.     , 6.35016, 0.     ],
            [0.     , 0.     , 6.35016]],
           [[6.35016, 0.     , 0.     ],
            [0.     , 6.35016, 0.     ],
            [0.     , 0.     , 6.35016]]])
    """
    import h5py

    print(f"Reading {os.path.abspath(hpath)} ...")
    hf = h5py.File(hpath)  # 加载h5文件
    Total_step = len(np.array(hf.get("/Structures"))) - 2  # 总步数

    if ele and ai:
        raise ValueError("暂不支持同时指定元素和原子序号")
    # 步数
    if index:
        if isinstance(index, int):  # 1
            indices = [index]

        elif isinstance(index, list) or isinstance(ai, np.ndarray):  # [1,2,3]
            indices = index

        elif isinstance(index, str):  # ':', '-3:'
            indices = _parse_indices(index, Total_step)

        else:
            raise ValueError("请输入正确格式的index")

        Nstep = len(indices)
    else:
        Nstep = Total_step
        indices = list(range(1, Nstep + 1))

    # 读取元素列表，这个列表不会随步数改变，也不会“合并同类项”
    from dspawpy.io.utils import get_ele_from_h5

    Elements = np.array(get_ele_from_h5(hpath), dtype="str")

    # 开始读取晶胞和原子位置
    lattices = np.empty((Nstep, 3, 3))  # Nstep x 3 x 3
    location = []
    if ele:  # 如果用户指定元素
        if isinstance(ele, str):  # 单个元素符号，例如 'Fe'
            ele_list = np.array(ele, dtype="str")
            location = np.where(Elements == ele_list)[0]
        # 多个元素符号组成的列表，例如 ['Fe', 'O']
        elif isinstance(ele, list) or isinstance(ele, np.ndarray):
            for e in ele:
                loc = np.where(Elements == e)[0]
                location.append(loc)
            location = np.concatenate(location)
        else:
            raise TypeError("请输入正确的元素或元素列表")
        elements = Elements[location]

    elif ai:  # 如果用户指定原子序号
        if isinstance(ai, int):  # 1
            ais = [ai]
        elif isinstance(ai, list) or isinstance(ai, np.ndarray):  # [1,2,3]
            ais = ai
        elif isinstance(ai, str):  # ':', '-3:'
            ais = _parse_indices(ai, Total_step)
        else:
            raise ValueError("请输入正确格式的ai")
        ais = [i - 1 for i in ais]  # python从0开始计数，但是用户从1开始计数
        elements = Elements[ais]
        location = ais

    else:  # 如果都没指定
        elements = Elements
        location = list(range(len(Elements)))

    elements = elements.tolist()  # for pretty output

    if return_scaled:
        scaled_positions = np.empty(shape=(len(indices), len(elements), 3))
        for i, index in enumerate(indices):  # 步数
            lats = np.array(hf.get("/Structures/Step-" + str(index) + "/Lattice"))
            lattices[i] = lats
            # [x1,y1,z1,x2,y2,z2,x3,y3,z3], ...
            # 结构优化时输出的都是分数坐标，不管CoordinateType写的是啥！
            spos = np.array(hf.get("/Structures/Step-" + str(index) + "/Position"))
            wrapped_spos = spos - np.floor(spos)  # wrap into [0,1)
            wrapped_spos = wrapped_spos.flatten().reshape(-1, 3).T  # reshape
            for j, sli in enumerate(location):
                scaled_positions[i, j, :] = np.dot(wrapped_spos[:, sli], np.eye(3, 3))
        return Nstep, elements, scaled_positions, lattices

    else:
        # Nstep x Natom x 3
        positions = np.empty(shape=(len(indices), len(elements), 3))
        for i, index in enumerate(indices):  # 步数
            lats = np.array(hf.get("/Structures/Step-" + str(index) + "/Lattice"))
            lattices[i] = lats
            # [x1,y1,z1,x2,y2,z2,x3,y3,z3], ...
            # 结构优化时输出的都是分数坐标，不管CoordinateType写的是啥！
            spos = np.array(hf.get("/Structures/Step-" + str(index) + "/Position"))
            wrapped_spos = spos - np.floor(spos)  # wrap into [0,1)
            wrapped_spos = wrapped_spos.flatten().reshape(-1, 3).T  # reshape
            for j, sli in enumerate(location):
                positions[i, j, :] = np.dot(wrapped_spos[:, sli], lats)

        return Nstep, elements, positions, lattices


# 2. 写轨迹文件
def write_xyz_traj(
    h5_path: str = "aimd.h5",
    jpath: str = None,
    ai=None,
    ele=None,
    index=None,
    xyzfile="aimdTraj.xyz",
):
    """保存xyz格式的轨迹文件

    Parameters
    ----------
    h5_path : str
        DSPAW计算完成后保存的h5文件路径
    jpath : str
        DSPAW计算完成后保存的json文件路径
    ai : int
        原子编号列表（体系中的第几号原子，不是质子数）
    ele : str
        元素，例如 'C'，'H'，'O'，'N'
    index : int
        优化过程中的第几步

    Returns
    -------
    xyzfile: str
        写入xyz格式的轨迹文件，默认为aimdTraj.xyz

    Example
    -------
    >>> from dspawpy.analysis.aimdtools import write_xyz_traj
    >>> write_xyz_traj(h5_path='aimd.h5', ai=[1,2,3], index=1, xyzfile='aimdTraj.xyz')
    """
    if jpath:
        Nstep, eles, poses, lats = _read_json(jpath, index, ele, ai)
    else:
        Nstep, eles, poses, lats = read_h5(h5_path, index, ele, ai)
    # 写入文件
    with open(xyzfile, "w") as f:
        # Nstep
        for n in range(Nstep):
            # 原子数不会变，就是不合并的元素总数
            f.write("%d\n" % len(eles))
            # lattice
            f.write(
                'Lattice="%f %f %f %f %f %f %f %f %f" Properties=species:S:1:pos:R:3 pbc="T T T"\n'
                % (
                    lats[n, 0, 0],
                    lats[n, 0, 1],
                    lats[n, 0, 2],
                    lats[n, 1, 0],
                    lats[n, 1, 1],
                    lats[n, 1, 2],
                    lats[n, 2, 0],
                    lats[n, 2, 1],
                    lats[n, 2, 2],
                )
            )
            # position and element
            for i in range(len(eles)):
                f.write(
                    "%s %f %f %f\n"
                    % (eles[i], poses[n, i, 0], poses[n, i, 1], poses[n, i, 2])
                )


def write_dump_traj(
    h5_path="aimd.h5",
    jpath=None,
    ai=None,
    ele=None,
    index=None,
    dumpfile="aimdTraj.dump",
):
    """保存为lammps的dump格式的轨迹文件，暂时只支持正交晶胞

    Parameters
    ----------
    h5_path : str
        DSPAW计算完成后保存的h5文件路径
    jpath : str
        DSPAW计算完成后保存的json文件路径
    ai : int
        原子编号列表（体系中的第几号原子，不是质子数）
    ele : str
        元素，例如 'C'，'H'，'O'，'N'
    index : int
        优化过程中的第几步

    Returns
    -------
    dumpfile: str
        写入xyz格式的轨迹文件，默认为aimdTraj.xyz

    Example
    -------
    >>> from dspawpy.analysis.aimdtools import write_dump_traj
    >>> write_dump_traj(h5_path='aimd.h5', ai=[1,2,3], index=1, dumpfile='aimdTraj.dump')
    """
    if jpath:
        Nstep, eles, poses, lats = _read_json(jpath, index, ele, ai)
    else:
        Nstep, eles, poses, lats = read_h5(h5_path, index, ele, ai)

    # 写入文件
    with open(dumpfile, "w") as f:
        for n in range(Nstep):
            box_bounds = _get_lammps_non_orthogonal_box(lats[n])
            f.write("ITEM: TIMESTEP\n%d\n" % n)
            f.write("ITEM: NUMBER OF ATOMS\n%d\n" % (len(eles)))
            f.write("ITEM: BOX BOUNDS xy xz yz xx yy zz\n")
            f.write(
                "%f %f %f\n%f %f %f\n %f %f %f\n"
                % (
                    box_bounds[0][0],
                    box_bounds[0][1],
                    box_bounds[0][2],
                    box_bounds[1][0],
                    box_bounds[1][1],
                    box_bounds[1][2],
                    box_bounds[2][0],
                    box_bounds[2][1],
                    box_bounds[2][2],
                )
            )
            f.write("ITEM: ATOMS type x y z id\n")
            for i in range(len(eles)):
                f.write(
                    "%s %f %f %f %d\n"
                    % (eles[i], poses[n, i, 0], poses[n, i, 1], poses[n, i, 2], i + 1)
                )


def _get_structure_list(df: str = "aimd.h5") -> List[Structure]:
    """get pymatgen structures from single datafile

    Parameters
    ----------
    df : str, optional
        datafile, by default "aimd.h5"

    Returns
    -------
    List[Structure] : list of pymatgen structures

    Examples
    --------
    >>> from dspawpy.analysis.aimdtools import get_structure_list
    >>> structure_list = get_structure_list(df='aimd.h5')
    """
    if df.endswith(".h5"):
        # create Structure structure_list from aimd.h5
        Nstep, elements, positions, lattices = read_h5(df)
        strs = []
        for i in range(Nstep):
            strs.append(
                Structure(
                    lattices[i], elements, positions[i], coords_are_cartesian=False
                )
            )
    elif df.endswith(".json"):
        from dspawpy.io.read import json2structures

        strs = json2structures(df)
    else:
        raise ValueError(f"{df} file format not supported")

    return strs


def _get_neighbor_list(structure, r) -> Tuple:
    """Thin wrapper to enable parallel calculations

    Parameter
    ---------
    structure (pymatgen Structure): pymatgen structure
    r (float): cutoff radius

    Returns
    --------
    tuple of neighbor list
    """
    return structure.get_neighbor_list(r)


def _parse_indices(index: str, total_step) -> list:
    """解析用户输入的原子序号字符串

    输入：
        - index: 用户输入的原子序号/元素字符串，例如 '1:3,5,7:10'
    输出：
        - indices: 解析后的原子序号列表，例如 [1,2,3,4,5,6,7,8,9,10]
    """
    assert ":" in index, "如果不想切片索引，请输入整数或者列表"
    blcs = index.split(",")
    indices = []
    for blc in blcs:
        if ":" in blc:  # 切片
            low = blc.split(":")[0]
            if not low:
                low = 1  # 从1开始
            else:
                low = int(low)
                assert low > 0, "索引从1开始！"
            high = blc.split(":")[1]
            if not high:
                high = total_step
            else:
                high = int(high)
                assert high <= total_step, "索引超出范围！"

            for i in range(low, high + 1):
                indices.append(i)
        else:  # 单个数字
            indices.append(int(blc))
    return indices


def _read_json(
    jpath: str,
    index= None,
    ele = None,
    ai= None,
):
    """从json指定的路径读取数据

    输入:
    - jpath: json文件路径
    - ai: 原子序号（体系中的第几个原子，不是质子数）
    - ele: 元素，例如 'C'，'H'，'O'，'N'
    - index: 运动轨迹中的第几步，从1开始

    输出：
    - Nstep: 总共要保存多少步的信息, int
    - elements: 元素列表, list, Natom x 1
    - positions: 原子位置, list, Nstep x Natom x 3
    - lattices: 晶胞, list, Nstep x 3 x 3
    """
    import json

    with open(jpath, "r") as f:
        data = json.load(f)  # 加载json文件

    Total_step = len(data["Structures"])  # 总步数

    if ele and ai:
        raise ValueError("暂不支持同时指定元素和原子序号")
    # 步数
    if index:
        if isinstance(index, int):  # 1
            indices = [index]

        elif isinstance(index, list) or isinstance(ai, np.ndarray):  # [1,2,3]
            indices = index

        elif isinstance(index, str):  # ':', '-3:'
            indices = _parse_indices(index, Total_step)

        else:
            raise ValueError("请输入正确格式的index")

        Nstep = len(indices)
    else:
        Nstep = Total_step
        indices = list(range(1, Nstep + 1))  # [1,Nstep+1)

    # 预先读取全部元素的总列表，这个列表不会随步数改变，也不会“合并同类项”
    # 这样可以避免在循环内部频繁判断元素是否符合用户需要

    Nele = len(data["Structures"][0]["Atoms"])  # 总元素数量
    total_elements = np.empty(shape=(Nele), dtype="str")  # 未合并的元素列表
    for i in range(Nele):
        element = data["Structures"][0]["Atoms"][i]["Element"]
        total_elements[i] = element

    # 开始读取晶胞和原子位置
    # 在data['Structures']['%d' % index]['Atoms']中根据元素所在序号选择结构
    if ele:  # 用户指定要某些元素
        location = []
        if isinstance(ele, str):  # 单个元素符号，例如 'Fe'
            ele_list = list(ele)
        # 多个元素符号组成的列表，例如 ['Fe', 'O']
        elif isinstance(ele, list) or isinstance(ele, np.ndarray):
            ele_list = ele
        else:
            raise TypeError("请输入正确的元素或元素列表")
        for e in ele_list:
            location.append(np.where(total_elements == e)[0])
        location = np.concatenate(location)

    elif ai:  # 如果用户指定原子序号，也要据此筛选元素列表
        if isinstance(ai, int):  # 1
            ais = [ai]
        elif isinstance(ai, list) or isinstance(ai, np.ndarray):  # [1,2,3]
            ais = ai
        elif isinstance(ai, str):  # ':', '-3:'
            ais = _parse_indices(ai, Total_step)
        else:
            raise ValueError("请输入正确格式的ai")
        ais = [i - 1 for i in ais]  # python从0开始计数，但是用户从1开始计数
        location = ais
        # read lattices and poses

    else:  # 如果都没指定
        location = list(range(Total_step))

    # 满足用户需要的elements列表
    elements = np.empty(shape=len(location), dtype="str")
    for i in range(len(location)):
        elements[i] = total_elements[location[i]]

    # Nstep x Natom x 3
    positions = np.empty(shape=(len(indices), len(elements), 3))
    lattices = np.empty(shape=(Nstep, 3, 3))  # Nstep x 3 x 3
    for i, index in enumerate(indices):  # 步数
        lat = data["Structures"][index - 1]["Lattice"]
        lattices[i] = np.array(lat).reshape(3, 3)
        for j, sli in enumerate(location):
            positions[i, j, :] = data["Structures"][index - 1]["Atoms"][sli][
                "Position"
            ][:]

    return Nstep, elements, positions, lattices


def _get_lammps_non_orthogonal_box(lat: np.ndarray):
    """计算用于输入lammps的盒子边界参数

    Parameters
    ----------
    lat : np.ndarray
        常见的非三角3x3矩阵

    Returns
    -------
    box_bounds:
        用于输入lammps的盒子边界
    """
    # https://docs.lammps.org/Howto_triclinic.html
    A = lat[0]
    B = lat[1]
    C = lat[2]
    assert np.cross(A, B).dot(C) > 0, "Lat is not right handed"

    # 将常规3x3矩阵转成标准的上三角矩阵
    alpha = np.arccos(np.dot(B, C) / (np.linalg.norm(B) * np.linalg.norm(C)))
    beta = np.arccos(np.dot(A, C) / (np.linalg.norm(A) * np.linalg.norm(C)))
    gamma = np.arccos(np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B)))

    ax = np.linalg.norm(A)
    a = np.array([ax, 0, 0])

    bx = np.linalg.norm(B) * np.cos(gamma)
    by = np.linalg.norm(B) * np.sin(gamma)
    b = np.array([bx, by, 0])

    cx = np.linalg.norm(C) * np.cos(beta)
    cy = (np.linalg.norm(B) * np.linalg.norm(C) - bx * cx) / by
    cz = np.sqrt(abs(np.linalg.norm(C) ** 2 - cx**2 - cy**2))
    c = np.array([cx, cy, cz])

    # triangluar matrix in lammmps cell format
    # note that in OVITO, it will be down-triangular one
    # lammps_lattice = np.array([a,b,c]).T

    # write lammps box parameters
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=The%20inverse%20relationship%20can%20be%20written%20as%20follows
    lx = np.linalg.norm(a)
    xy = np.linalg.norm(b) * np.cos(gamma)
    xz = np.linalg.norm(c) * np.cos(beta)
    ly = np.sqrt(np.linalg.norm(b) ** 2 - xy**2)
    yz = (np.linalg.norm(b) * np.linalg.norm(c) * np.cos(alpha) - xy * xz) / ly
    lz = np.sqrt(np.linalg.norm(c) ** 2 - xz**2 - yz**2)

    # "The parallelepiped has its “origin” at (xlo,ylo,zlo) and is defined by 3 edge vectors starting from the origin given by a = (xhi-xlo,0,0); b = (xy,yhi-ylo,0); c = (xz,yz,zhi-zlo)."
    # 令原点在(0,0,0)，则 xlo = ylo = zlo = 0
    xlo = ylo = zlo = 0
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=the%20LAMMPS%20box%20sizes%20(lx%2Cly%2Clz)%20%3D%20(xhi%2Dxlo%2Cyhi%2Dylo%2Czhi%2Dzlo)
    xhi = lx + xlo
    yhi = ly + ylo
    zhi = lz + zlo
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=This%20bounding%20box%20is%20convenient%20for%20many%20visualization%20programs%20and%20is%20calculated%20from%20the%209%20triclinic%20box%20parameters%20(xlo%2Cxhi%2Cylo%2Cyhi%2Czlo%2Czhi%2Cxy%2Cxz%2Cyz)%20as%20follows%3A
    xlo_bound = xlo + np.min([0, xy, xz, xy + xz])
    xhi_bound = xhi + np.max([0, xy, xz, xy + xz])
    ylo_bound = ylo + np.min([0, yz])
    yhi_bound = yhi + np.max([0, yz])
    zlo_bound = zlo
    zhi_bound = zhi
    box_bounds = np.array(
        [
            [xlo_bound, xhi_bound, xy],
            [ylo_bound, yhi_bound, xz],
            [zlo_bound, zhi_bound, yz],
        ]
    )

    return box_bounds

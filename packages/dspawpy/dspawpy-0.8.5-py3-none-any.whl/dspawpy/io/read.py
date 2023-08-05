# -*- coding: utf-8 -*-

import json
import h5py
from typing import List, Dict

import numpy as np
from pymatgen.core.structure import Structure
from pymatgen.core.lattice import Lattice
from pymatgen.electronic_structure.dos import Dos, CompleteDos
from pymatgen.electronic_structure.core import Spin
from pymatgen.electronic_structure.core import Orbital
from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine
from pymatgen.phonon.bandstructure import PhononBandStructureSymmLine
from pymatgen.phonon.dos import PhononDos


def json2structures(jsonfile):
    """relax.json/aimd.json -> [pymatgen.Structure]

    Parameters
    ----------
    jsonfile : str
        包含多个离子步的 json 文件路径，例如 "relax.json" 或 "aimd.json"

    Returns
    -------
    pymatgen_structures : list
        pymatgen.Structure 列表

    Examples
    --------
    >>> from dspawpy.io.read import json2structures
    >>> structures = json2structures("relax.json")
    """
    with open(jsonfile, "r") as file:
        j = json.load(file)

    pymatgen_structures = []
    for step in range(len(j)):
        atominfo = j[step]["Atoms"]
        elements = []
        positions = []
        for atomindex in range(len(atominfo)):
            elements.append(atominfo[atomindex]["Element"])
            positions.append(atominfo[atomindex]["Position"])
        coords = np.asarray(positions).reshape(-1, 3)
        lattice = np.asarray(j[step]["Lattice"]).reshape(3, 3)
        pymatgen_structures.append(
            Structure(lattice, elements, coords, coords_are_cartesian=True)
        )

    return pymatgen_structures


def load_h5(dir_h5: str) -> dict:
    """遍历读取h5文件中的数据，保存为字典格式

    慎用此函数，因为会读取很多不需要的数据，耗时很长。

    Parameters
    ----------
    dir_h5 : str
        h5文件路径

    Returns
    -------
    datas: dict
        数据字典

    Examples
    --------
    >>> from dspawpy.io.read import load_h5
    >>> datas = load_h5(dir_h5)
    """

    def get_names(key, h5_object):
        names.append(h5_object.name)

    def is_dataset(name):
        for name_inTheList in names:
            if name_inTheList.find(name + "/") != -1:
                return False
        return True

    def get_datas(key, h5_object):
        if is_dataset(h5_object.name):
            data = np.asarray(h5_object)
            if data.dtype == "|S1":  # 转成字符串 并根据";"分割
                byte2str = [str(bi, "utf-8") for bi in data]
                string = ""
                for char in byte2str:
                    string += char
                data = np.array([elem for elem in string.strip().split(";")])
            # "/group1/group2/.../groupN/dataset" : value
            datas[h5_object.name] = data.tolist()

    with h5py.File(dir_h5, "r") as fin:
        names = []
        datas = {}
        fin.visititems(get_names)
        fin.visititems(get_datas)

        return datas


def load_h5_todict(dir_h5: str) -> Dict:
    """与上一个函数区别在于合并了部分同类数据，例如

    /Structures/Step-1/* 和 /Structures/Step-2/* 并入 /Structures/ 组内
    """

    def create_dict(L: List, D: Dict):
        if len(L) == 2:
            D[L[0]] = L[1]
            return
        else:
            if not (L[0] in D.keys()):
                D[L[0]] = {}
            create_dict(L[1:], D[L[0]])

    datas = load_h5(dir_h5)

    groups_value_list = []
    for key in datas.keys():
        tmp_list = key[1:].strip().split("/")  # [1:] 截去root
        tmp_list.append(datas[key])
        # groups_value_list[i]结构: [group1, group2, ..., groupN, dataset, value]
        groups_value_list.append(tmp_list)

    groups_value_dict = {}
    for data in groups_value_list:
        create_dict(data, groups_value_dict)

    return groups_value_dict


def get_dos_data(dos_dir: str):
    if dos_dir.endswith(".h5"):
        dos = load_h5(dos_dir)
        if dos["/DosInfo/Project"][0]:
            return get_complete_dos(dos)
        else:
            return get_total_dos(dos)

    elif dos_dir.endswith(".json"):
        with open(dos_dir, "r") as fin:
            dos = json.load(fin)

        if dos["DosInfo"]["Project"]:
            return get_complete_dos_json(dos)
        else:
            return get_total_dos_json(dos)

    else:
        print("file - " + dos_dir + " :  Unsupported format!")
        return


def get_total_dos(dos: Dict) -> Dos:
    # h5 -> Dos Obj
    energies = np.asarray(dos["/DosInfo/DosEnergy"])
    if dos["/DosInfo/SpinType"][0] == "none":
        densities = {Spin.up: np.asarray(dos["/DosInfo/Spin1/Dos"])}
    else:
        densities = {
            Spin.up: np.asarray(dos["/DosInfo/Spin1/Dos"]),
            Spin.down: np.asarray(dos["/DosInfo/Spin2/Dos"]),
        }

    efermi = dos["/DosInfo/EFermi"][0]

    return Dos(efermi, energies, densities)


def get_complete_dos(dos: Dict) -> CompleteDos:
    # h5 -> CompleteDos Obj
    total_dos = get_total_dos(dos)
    structure = get_structure(dos, "/AtomInfo")
    N = len(structure)
    pdos = [{} for i in range(N)]
    number_of_spin = 1 if dos["/DosInfo/SpinType"][0] == "none" else 2

    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down
        atomindexs = dos["/DosInfo/" + spin_key + "/ProjectDos/AtomIndexs"][0]
        orbitindexs = dos["/DosInfo/" + spin_key + "/ProjectDos/OrbitIndexs"][0]
        for atom_index in range(atomindexs):
            for orbit_index in range(orbitindexs):
                orbit_name = Orbital(orbit_index)
                Contribution = dos[
                    "/DosInfo/"
                    + spin_key
                    + "/ProjectDos"
                    + str(atom_index + 1)
                    + "/"
                    + str(orbit_index + 1)
                ]
                if orbit_name in pdos[atom_index].keys():
                    pdos[atom_index][orbit_name].update({spin: Contribution})
                else:
                    pdos[atom_index][orbit_name] = {spin: Contribution}

    pdoss = {structure[i]: pd for i, pd in enumerate(pdos)}

    return CompleteDos(structure, total_dos, pdoss)


def get_total_dos_json(dos: Dict) -> Dos:
    # json -> Dos Obj
    energies = np.asarray(dos["DosInfo"]["DosEnergy"])
    if dos["DosInfo"]["SpinType"] == "none":
        densities = {Spin.up: np.asarray(dos["DosInfo"]["Spin1"]["Dos"])}
    else:
        densities = {
            Spin.up: np.asarray(dos["DosInfo"]["Spin1"]["Dos"]),
            Spin.down: np.asarray(dos["DosInfo"]["Spin2"]["Dos"]),
        }
    efermi = dos["DosInfo"]["EFermi"]
    return Dos(efermi, energies, densities)


def get_complete_dos_json(dos: Dict) -> CompleteDos:
    # json -> CompleteDos Obj
    total_dos = get_total_dos_json(dos)
    structure = get_structure_json(dos["AtomInfo"])
    N = len(structure)
    pdos = [{} for i in range(N)]
    number_of_spin = 1 if dos["DosInfo"]["SpinType"] == "none" else 2

    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down
        project = dos["DosInfo"][spin_key]["ProjectDos"]
        for p in project:
            atom_index = p["AtomIndex"] - 1
            o = p["OrbitIndex"] - 1
            orbit_name = Orbital(o)
            if orbit_name in pdos[atom_index].keys():
                pdos[atom_index][orbit_name].update({spin: p["Contribution"]})
            else:
                pdos[atom_index][orbit_name] = {spin: p["Contribution"]}
    pdoss = {structure[i]: pd for i, pd in enumerate(pdos)}

    return CompleteDos(structure, total_dos, pdoss)


def get_structure(hdf5: Dict, key: str) -> Structure:
    # load_h5 -> Structure Obj
    lattice = np.asarray(hdf5[key + "/Lattice"]).reshape(3, 3)
    elements = hdf5[key + "/Elements"]
    positions = hdf5[key + "/Position"]
    coords = np.asarray(positions).reshape(-1, 3)
    is_direct = hdf5[key + "/CoordinateType"][0] == "Direct"
    return Structure(lattice, elements, coords, coords_are_cartesian=(not is_direct))


def get_structure_json(atominfo) -> Structure:
    lattice = np.asarray(atominfo["Lattice"]).reshape(3, 3)
    elements = []
    positions = []
    for atom in atominfo["Atoms"]:
        elements.append(atom["Element"])
        positions.extend(atom["Position"])

    coords = np.asarray(positions).reshape(-1, 3)
    is_direct = atominfo["CoordinateType"] == "Direct"
    return Structure(lattice, elements, coords, coords_are_cartesian=(not is_direct))


def get_structure_from_json(jsonfile: str) -> Structure:
    with open(jsonfile, "r") as file:
        j = json.load(file)
    lattice = np.asarray(j["AtomInfo"]["Lattice"]).reshape(3, 3)
    elements = j["AtomInfo"]["Elements"]
    positions = j["AtomInfo"]["Position"]
    coords = np.asarray(positions).reshape(-1, 3)
    is_direct = j["AtomInfo"]["CoordinateType"][0] == "Direct"
    return Structure(lattice, elements, coords, coords_are_cartesian=(not is_direct))


def get_band_data_h5(band: Dict, iwan=False):
    if iwan:
        bd = "WannBandInfo"
    else:
        bd = "BandInfo"
    number_of_band = band[f"/{bd}/NumberOfBand"][0]
    number_of_kpoints = band[f"/{bd}/NumberOfKpoints"][0]
    if (
        band[f"/{bd}/SpinType"][0] == "none"
        or band[f"/{bd}/SpinType"][0] == "non-collinear"
    ):
        number_of_spin = 1
    else:
        number_of_spin = 2

    symmetry_kPoints_index = band[f"/{bd}/SymmetryKPointsIndex"]

    efermi = band[f"/{bd}/EFermi"][0]
    eigenvals = {}
    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down

        if f"/{bd}/" + spin_key + "/BandEnergies" in band:
            data = band[f"/{bd}/" + spin_key + "/BandEnergies"]
        elif f"/{bd}/" + spin_key + "/Band" in band:
            data = band[f"/{bd}/" + spin_key + "/Band"]
        else:
            print("Band key error")
            return
        band_data = np.array(data).reshape((number_of_kpoints, number_of_band)).T
        eigenvals[spin] = band_data

    kpoints = np.asarray(band[f"/{bd}/CoordinatesOfKPoints"]).reshape(
        number_of_kpoints, 3
    )

    structure = get_structure(band, "/AtomInfo")
    labels_dict = {}

    for i, s in enumerate(band[f"/{bd}/SymmetryKPoints"]):
        labels_dict[s] = kpoints[symmetry_kPoints_index[i] - 1]

    # read projection data
    projections = None
    if f"/{bd}/IsProject" in band.keys():
        if band[f"/{bd}/IsProject"][0]:
            projections = {}
            number_of_orbit = len(band[f"/{bd}/Orbit"])
            projection = np.zeros(
                (number_of_band, number_of_kpoints, number_of_orbit, len(structure))
            )

            for i in range(number_of_spin):
                spin_key = "Spin" + str(i + 1)
                spin = Spin.up if i == 0 else Spin.down

                atomindexs = band[f"/{bd}/" + spin_key + "/ProjectBand/AtomIndex"][0]
                orbitindexs = band[f"/{bd}/" + spin_key + "/ProjectBand/OrbitIndexs"][0]
                for atom_index in range(atomindexs):
                    for orbit_index in range(orbitindexs):
                        project_data = band[
                            f"/{bd}/"
                            + spin_key
                            + "/ProjectBand/1/"
                            + str(atom_index + 1)
                            + "/"
                            + str(orbit_index + 1)
                        ]
                        projection[:, :, orbit_index, atom_index] = (
                            np.asarray(project_data)
                            .reshape((number_of_kpoints, number_of_band))
                            .T
                        )
                projections[spin] = projection

    return structure, kpoints, eigenvals, efermi, labels_dict, projections


def get_band_data_json(band: Dict, iwan=False):
    if iwan:
        bd = "WannBandInfo"
    else:
        bd = "BandInfo"

    number_of_band = band[f"{bd}"]["NumberOfBand"]
    number_of_kpoints = band[f"{bd}"]["NumberOfKpoints"]
    if 'Spin2' in band[f"{bd}"]:
        number_of_spin = 2
    else:
        number_of_spin = 1

    symmetry_kPoints_index = band[f"{bd}"]["SymmetryKPointsIndex"]

    if "EFermi" in band[f"{bd}"]:
        efermi = band[f"{bd}"]["EFermi"]
    else:
        efermi = 0 # for wannier
        
    eigenvals = {}
    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down

        if "BandEnergies" in band[f"{bd}"][spin_key]:
            data = band[f"{bd}"][spin_key]["BandEnergies"]
        elif "Band" in band[f"{bd}"][spin_key]:
            data = band[f"{bd}"][spin_key]["Band"]
        else:
            print("Band key error")
            return

        band_data = np.array(data).reshape((number_of_kpoints, number_of_band)).T

        eigenvals[spin] = band_data

    kpoints = np.asarray(band[f"{bd}"]["CoordinatesOfKPoints"]).reshape(
        number_of_kpoints, 3
    )

    structure = get_structure_json(band["AtomInfo"])
    labels_dict = {}

    for i, s in enumerate(band[f"{bd}"]["SymmetryKPoints"]):
        labels_dict[s] = kpoints[symmetry_kPoints_index[i] - 1]

    # read projection data
    projections = None
    if "IsProject" in band[f"{bd}"].keys():
        if band[f"{bd}"]["IsProject"]:
            projections = {}
            number_of_orbit = len(band[f"{bd}"]["Orbit"])
            projection = np.zeros(
                (number_of_band, number_of_kpoints, number_of_orbit, len(structure))
            )

            for i in range(number_of_spin):
                spin_key = "Spin" + str(i + 1)
                spin = Spin.up if i == 0 else Spin.down

                data = band[f"{bd}"][spin_key]["ProjectBand"]
                for d in data:
                    orbit_index = d["OrbitIndex"] - 1
                    atom_index = d["AtomIndex"] - 1
                    project_data = d["Contribution"]
                    projection[:, :, orbit_index, atom_index] = (
                        np.asarray(project_data)
                        .reshape((number_of_kpoints, number_of_band))
                        .T
                    )

                projections[spin] = projection

    return structure, kpoints, eigenvals, efermi, labels_dict, projections


def get_band_data(band_dir: str, efermi: float = None) -> BandStructureSymmLine:
    # modify BandStructureSymmLine.efermi after it was created will cause error
    if band_dir.endswith(".h5"):
        band = load_h5(band_dir)
        raw = h5py.File(band_dir, "r").keys()
        if "/WannBandInfo/NumberOfBand" in raw:
            (
                structure,
                kpoints,
                eigenvals,
                efermi,
                labels_dict,
                projections,
            ) = get_band_data_h5(band, iwan=True)
        elif "/BandInfo/NumberOfBand" in raw:
            (
                structure,
                kpoints,
                eigenvals,
                efermi,
                labels_dict,
                projections,
            ) = get_band_data_h5(band, iwan=False)
        else:
            print("BandInfo or WannBandInfo key not found in h5file!")
            return
    elif band_dir.endswith(".json"):
        with open(band_dir, "r") as fin:
            band = json.load(fin)
        if "WannBandInfo" in band.keys():
            (
                structure,
                kpoints,
                eigenvals,
                efermi,
                labels_dict,
                projections,
            ) = get_band_data_json(band, iwan=True)
        elif "BandInfo" in band.keys():
            (
                structure,
                kpoints,
                eigenvals,
                efermi,
                labels_dict,
                projections,
            ) = get_band_data_json(band, iwan=False)
        else:
            print("BandInfo or WannBandInfo key not found in json file!")
            return
    else:
        print("file - " + band_dir + " :  Unsupported format!")
        return

    if efermi:  # 从h5直接读取的费米能级可能是错的，此时需要用户自行指定
        efermi = efermi  # 这只是个临时解决方案

    lattice_new = Lattice(structure.lattice.reciprocal_lattice.matrix)
    return BandStructureSymmLine(
        kpoints=kpoints,
        eigenvals=eigenvals,
        lattice=lattice_new,
        efermi=efermi,
        labels_dict=labels_dict,
        structure=structure,
        projections=projections,
    )


def get_phonon_band_data_h5(band: Dict):
    number_of_band = band["/BandInfo/NumberOfBand"][0]
    number_of_kpoints = band["/BandInfo/NumberOfQPoints"][0]
    number_of_spin = 1
    symmmetry_kpoints = band["/BandInfo/SymmetryQPoints"]
    symmetry_kPoints_index = band["/BandInfo/SymmetryQPointsIndex"]
    eigenvals = {}
    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down
        if "/BandInfo/" + spin_key + "/BandEnergies" in band:
            data = band["/BandInfo/" + spin_key + "/BandEnergies"]
        elif "/BandInfo/" + spin_key + "/Band" in band:
            data = band["/BandInfo/" + spin_key + "/Band"]
        else:
            print("Band key error")
            return
        frequencies = np.array(data).reshape((number_of_kpoints, number_of_band)).T
        eigenvals[spin] = frequencies
    kpoints = np.asarray(band["/BandInfo/CoordinatesOfQPoints"]).reshape(
        number_of_kpoints, 3
    )
    if "/SupercellAtomInfo/CoordinateType" in band.keys():
        structure = get_structure(band, "/SupercellAtomInfo")
    else:
        structure = get_structure(band, "/AtomInfo")
    return symmmetry_kpoints, symmetry_kPoints_index, kpoints, structure, frequencies


def get_phonon_band_data_json(band: Dict):
    number_of_band = band["BandInfo"]["NumberOfBand"]
    number_of_kpoints = band["BandInfo"]["NumberOfQPoints"]
    number_of_spin = 1
    symmmetry_kpoints = band["BandInfo"]["SymmetryQPoints"]
    symmetry_kPoints_index = band["BandInfo"]["SymmetryQPointsIndex"]

    eigenvals = {}
    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down
        if "BandEnergies" in band["BandInfo"][spin_key]:
            data = band["BandInfo"][spin_key]["BandEnergies"]
        elif "Band" in band["BandInfo"][spin_key]:
            data = band["BandInfo"][spin_key]["Band"]
        else:
            print("Band key error")
            return
        frequencies = np.array(data).reshape((number_of_kpoints, number_of_band)).T
        eigenvals[spin] = frequencies

    kpoints = np.asarray(band["BandInfo"]["CoordinatesOfQPoints"]).reshape(
        number_of_kpoints, 3
    )

    if "SupercellAtomInfo" in band.keys():
        structure = get_structure_json(band["SupercellAtomInfo"])
    else:
        structure = get_structure_json(band["AtomInfo"])

    return symmmetry_kpoints, symmetry_kPoints_index, kpoints, structure, frequencies


def get_phonon_band_data(phonon_band_dir: str) -> PhononBandStructureSymmLine:
    if phonon_band_dir.endswith(".h5"):
        band = load_h5(phonon_band_dir)
        (
            symmmetry_kpoints,
            symmetry_kPoints_index,
            kpoints,
            structure,
            frequencies,
        ) = get_phonon_band_data_h5(band)
    elif phonon_band_dir.endswith(".json"):
        with open(phonon_band_dir, "r") as fin:
            band = json.load(fin)
        (
            symmmetry_kpoints,
            symmetry_kPoints_index,
            kpoints,
            structure,
            frequencies,
        ) = get_phonon_band_data_json(band)
    else:
        print("file - " + phonon_band_dir + " :  Unsupported format!")
        return

    labels_dict = {}
    for i, s in enumerate(symmmetry_kpoints):
        labels_dict[s] = kpoints[symmetry_kPoints_index[i] - 1]
    lattice_new = Lattice(structure.lattice.reciprocal_lattice.matrix)

    return PhononBandStructureSymmLine(
        qpoints=kpoints,
        frequencies=frequencies,
        lattice=lattice_new,
        has_nac=False,
        labels_dict=labels_dict,
        structure=structure,
    )


def get_phonon_dos_data(phonon_dos_dir: str) -> PhononDos:
    if phonon_dos_dir.endswith(".h5"):
        dos = load_h5(phonon_dos_dir)
        frequencies = np.asarray(dos["/DosInfo/DosEnergy"])
        densities = dos["/DosInfo/Spin1/Dos"]
    elif phonon_dos_dir.endswith(".json"):
        with open(phonon_dos_dir, "r") as fin:
            dos = json.load(fin)
        frequencies = np.asarray(dos["DosInfo"]["DosEnergy"])
        densities = dos["DosInfo"]["Spin1"]["Dos"]
    else:
        print("file - " + phonon_dos_dir + " :  Unsupported format!")
        return

    return PhononDos(frequencies, densities)

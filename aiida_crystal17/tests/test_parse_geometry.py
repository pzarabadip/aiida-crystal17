"""
test reading/creating .gui files
for EXTERNAL keyword use
"""
import os

from aiida_crystal17.tests import TEST_DIR
import numpy as np
import pytest
from aiida_crystal17.parsers.geometry import read_gui_file, compute_symmetry, get_centering_code, get_crystal_system, \
    create_gui_from_ase, crystal17_gui_string
from ase.spacegroup import crystal
from jsonextended import edict


@pytest.fixture(scope="function")
def default_settings():
    return {
        "crystal": {
            "system": "triclinic",
            "transform": None,
        },
        "symmetry": {
            "symprec": 0.01,
            "angletol": None,
            "operations": None,
            "sgnum": 1,
        },
        "3d": {
            "standardize": True,
            "primitive": True,
            "idealize": False
        }
    }


@pytest.mark.parametrize(
    "sg_num,sg_symbol,centering,crystal_type",
    [
        (15, "C2/c", 4, 2),  # pyrrhotite-4c
        (205, 'Pa3', 1, 6),  # pyrite
        (58, 'Pnnm', 1, 3),  # marcasite
        (190, 'P-62c', 1, 5),  # troilite
        (129, 'P4/nmm', 1,
         4),  # mackinawite (origin choice 2) CENTRING CODE 1/1
        (227, 'Fd3m', 5, 6)  # greigite
    ])
def test_get_centering_code(sg_num, sg_symbol, centering, crystal_type):
    assert get_crystal_system(sg_num, as_number=True) == crystal_type
    assert get_centering_code(sg_num, sg_symbol) == centering


def test_read_gui_file():
    inpath = os.path.join(TEST_DIR, "input_files",
                          'mgo_sto3g_external.crystal.gui')
    data = read_gui_file(inpath)

    expected = {
        'natoms':
        2,
        'lattice': [[0.0, 2.105, 2.105], [2.105, 0.0, 2.105],
                    [2.105, 2.105, 0.0]],
        'pbc': [True, True, True],
        'crystal_type':
        'cubic',
        'origin_setting':
        5,
        'ccoords': [[0.0, 0.0, 0.0], [2.105, 2.105, 2.105]],
        'atomic_numbers': [12, 8],
        'nsymops':
        48,
        'symops':
        [[1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
          0.0], [-1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
         [1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0,
          0.0], [-1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0],
         [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0,
          0.0], [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              0.0, 0.0, -1.0, -1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, -1.0, 0.0, 0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, -1.0, 0.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, 1.0, 0.0, 0.0, 0.0, -1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              0.0, -1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0
          ], [0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0], [
              0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0
          ], [0.0, -1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0], [
              -1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, 0.0, -1.0, 0.0, -1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, 0.0, -1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, 0.0, 1.0, 0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              -1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, 0.0, 1.0, 0.0, -1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              -1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0
          ], [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0], [
              -1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0
          ], [1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0], [
              0.0, 0.0, -1.0, -1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, -1.0, 0.0, 0.0, 0.0, -1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, 1.0, 0.0, 0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              0.0, 0.0, -1.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, 1.0, 0.0, 0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              0.0, 0.0, 1.0, -1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, -1.0, 0.0, 0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0
          ], [0.0, -1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0], [
              0.0, -1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0
          ], [0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0], [
              1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              -1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, 0.0, 1.0, 0.0, -1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              -1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, 0.0, -1.0, 0.0, -1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], [
              1.0, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0
          ], [0.0, 0.0, -1.0, 0.0, 1.0, 0.0, -1.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    }

    assert edict.diff(data, expected) == {}


def test_write_gui_with_symops(default_settings):
    sdata = {
        "lattice": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        "ccoords": [[0, 0, 0]],
        "atomic_numbers": [1],
        "pbc": [True, True, True],
        "equivalent": [0]
    }
    symops = [[1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0]]  # i.e. no symmetry

    default_settings["symmetry"]["operations"] = symops

    outsdata, symmdata = compute_symmetry(sdata, default_settings)
    outstr = crystal17_gui_string(outsdata, symmdata)

    expected = """3 1 1
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
1
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
1
  1   0.000000000E+00   0.000000000E+00   0.000000000E+00
1 1
"""
    assert outstr == expected
    assert outsdata == sdata


def test_write_gui_without_symops(default_settings):
    sdata = {
        "lattice": [[2, 0, 0], [0, 2, 0], [0, 0, 2]],
        "ccoords": [[1, 1, 1]],
        "atomic_numbers": [5],
        "pbc": [True, True, True],
        "equivalent": [0]
    }

    outsdata, symmdata = compute_symmetry(sdata, default_settings)
    outstr = crystal17_gui_string(outsdata, symmdata)

    expected = """3 1 6
  2.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   2.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   2.000000000E+00
48
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
1
  5   1.000000000E+00   1.000000000E+00   1.000000000E+00
221 48
"""
    assert edict.diff(outsdata, sdata, np_allclose=True) == {}
    assert outstr == expected


def test_write_gui_mgo_nonprimitive(default_settings):
    # MgO
    atoms = crystal(
        symbols=[12, 8],
        basis=[[0, 0, 0], [0.5, 0.5, 0.5]],
        spacegroup=225,
        cellpar=[4.21, 4.21, 4.21, 90, 90, 90])

    default_settings["3d"]["primitive"] = False
    default_settings["3d"]["standardize"] = False
    outstr, outatoms = create_gui_from_ase(atoms, default_settings)

    assert np.allclose(atoms.cell, outatoms.cell)
    assert atoms.get_number_of_atoms() == outatoms.get_number_of_atoms()


def test_write_gui_mgo_primitive(default_settings):
    # MgO
    atoms = crystal(
        symbols=[12, 8],
        basis=[[0, 0, 0], [0.5, 0.5, 0.5]],
        spacegroup=225,
        cellpar=[4.21, 4.21, 4.21, 90, 90, 90])

    outstr, outatoms = create_gui_from_ase(atoms, default_settings)

    expected = """3 5 6
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
 -2.105000000E+00  -2.105000000E+00   0.000000000E+00
 -2.105000000E+00   0.000000000E+00  -2.105000000E+00
48
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
 -2.105000000E+00   0.000000000E+00  -2.105000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
 -2.105000000E+00  -4.210000000E+00  -2.105000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
 -2.105000000E+00   0.000000000E+00  -2.105000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
 -2.105000000E+00  -4.210000000E+00  -2.105000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
 -2.105000000E+00   0.000000000E+00  -2.105000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
 -2.105000000E+00  -4.210000000E+00  -2.105000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
 -2.105000000E+00  -2.105000000E+00  -4.210000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
 -2.105000000E+00   0.000000000E+00  -2.105000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
 -2.105000000E+00  -2.105000000E+00  -4.210000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
 -2.105000000E+00  -4.210000000E+00  -2.105000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
 -2.105000000E+00  -2.105000000E+00  -4.210000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
 -2.105000000E+00  -2.105000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
 -2.105000000E+00  -2.105000000E+00  -4.210000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
 -2.105000000E+00  -2.105000000E+00  -4.210000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
 -2.105000000E+00  -2.105000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
 -2.105000000E+00  -2.105000000E+00  -4.210000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00  -2.105000000E+00  -2.105000000E+00
2
 12  -2.105000000E+00  -2.105000000E+00  -4.210000000E+00
  8  -2.105000000E+00  -2.105000000E+00  -2.105000000E+00
225 48
"""

    assert outstr == expected
    assert np.allclose(
        outatoms.cell,
        [[0, -2.105, -2.105], [-2.105, -2.105, 0], [-2.105, 0, -2.105]])
    assert outatoms.get_atomic_numbers().tolist() == [12, 8]


def test_write_gui_marcasite(default_settings):
    """has irregular order of lengths, primitive == crystallographic"""
    atoms = crystal(
        symbols=[26, 16],
        basis=[[0, 0, 0], [0.20052, 0.37827, 0.0]],
        spacegroup=58,
        cellpar=[4.57072239, 5.60859256, 3.50105841, 90, 90, 90])

    outstr, outatoms = create_gui_from_ase(atoms, default_settings)

    expected = """3 1 3
  4.570722390E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   5.608592560E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   3.501058410E+00
8
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  2.285361195E+00   2.804296280E+00   1.750529205E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  2.285361195E+00   2.804296280E+00   1.750529205E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  2.285361195E+00   2.804296280E+00   1.750529205E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  2.285361195E+00   2.804296280E+00   1.750529205E+00
6
 26   0.000000000E+00   0.000000000E+00   0.000000000E+00
 26   2.285361195E+00   2.804296280E+00   1.750529205E+00
 16   9.165212536E-01   2.121562308E+00   0.000000000E+00
 16   3.654201136E+00   3.487030252E+00   0.000000000E+00
 16   1.368839941E+00   4.925858588E+00   1.750529205E+00
 16   3.201882449E+00   6.827339723E-01   1.750529205E+00
58 8
"""

    assert atoms.positions == pytest.approx(outatoms.positions)
    assert outstr == expected


def test_write_gui_mgo_inequivalent(default_settings):
    # MgO
    atoms = crystal(
        symbols=[12, 8],
        basis=[[0, 0, 0], [0.5, 0.5, 0.5]],
        spacegroup=225,
        cellpar=[4.21, 4.21, 4.21, 90, 90, 90])

    atoms.set_tags([1, 1, 0, 0, 0, 0, 0, 0])

    outstr, outatoms = create_gui_from_ase(atoms, default_settings)

    print(outstr)

    expected = """3 1 4
  0.000000000E+00   2.105000000E+00  -2.105000000E+00
  0.000000000E+00   2.105000000E+00   2.105000000E+00
  4.210000000E+00   0.000000000E+00   0.000000000E+00
16
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   2.105000000E+00  -2.105000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   2.105000000E+00  -2.105000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   2.105000000E+00  -2.105000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   2.105000000E+00  -2.105000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   2.105000000E+00  -2.105000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   2.105000000E+00  -2.105000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   2.105000000E+00  -2.105000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
 -1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00   1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00  -1.000000000E+00
  0.000000000E+00   2.105000000E+00  -2.105000000E+00
  1.000000000E+00   0.000000000E+00   0.000000000E+00
  0.000000000E+00  -1.000000000E+00   0.000000000E+00
  0.000000000E+00   0.000000000E+00   1.000000000E+00
  0.000000000E+00   0.000000000E+00   0.000000000E+00
4
 12   4.094618574E-32   2.105000000E+00  -2.105000000E+00
 12   2.105000000E+00   2.105000000E+00   6.661338148E-16
  8   2.105000000E+00   2.105000000E+00  -2.105000000E+00
  8   1.288940756E-16   2.105000000E+00   6.661338148E-16
123 16
"""

    assert outstr == expected
    assert np.allclose(outatoms.cell,
                       [[0, 2.105, -2.105], [0, 2.105, 2.105], [4.21, 0, 0]])
    assert outatoms.get_atomic_numbers().tolist() == [12, 12, 8, 8]
    assert outatoms.get_tags().tolist() == [1, 0, 0, 0]

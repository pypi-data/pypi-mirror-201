# BioPandas
# Author: Arian Jamasb <arian@jamasb.io> Sebastian Raschka <mail@sebastianraschka.com>
# License: BSD 3 clause
# Project Website: http://rasbt.github.io/biopandas/
# Code Repository: https://github.com/rasbt/biopandas

import os

from biopandas.mmcif import PandasMmcif
from nose.tools import raises

TESTDATA_1t48 = os.path.join(os.path.dirname(__file__), "data", "1t48.cif")
TESTDATA_1t49 = os.path.join(os.path.dirname(__file__), "data", "1t49.cif")
# TESTDATA_lig1 = os.path.join(os.path.dirname(__file__), "data", "lig_conf_1.pdb")
# TESTDATA_lig2 = os.path.join(os.path.dirname(__file__), "data", "lig_conf_2.pdb")

TESTDATA_rna = os.path.join(os.path.dirname(__file__), "data", "1ehz.cif")

p1t48 = PandasMmcif()
p1t48.read_mmcif(TESTDATA_1t48)
p1t49 = PandasMmcif()
p1t49.read_mmcif(TESTDATA_1t49)

# pl1 = PandasPdb()
# pl1.read_pdb(TESTDATA_lig1)
# pl2 = PandasPdb()
# pl2.read_pdb(TESTDATA_lig2)


def test_equal():
    r = PandasMmcif.rmsd(p1t48.df["ATOM"], p1t48.df["ATOM"], s=None)
    assert r == 0.000, r


@raises(AttributeError)
def test_wrong_arg():
    PandasMmcif.rmsd(p1t48.df["ATOM"].loc[1:, :], p1t48.df["ATOM"], s="bla")


@raises(AttributeError)
def test_incompatible():
    PandasMmcif.rmsd(p1t48.df["ATOM"].loc[1:, :], p1t48.df["ATOM"], s=None)


@raises(AttributeError)
def test_invalid_query():
    PandasMmcif.rmsd(p1t48.df["ATOM"].loc[1:, :], p1t48.df["ATOM"], s="bla")


def test_protein():
    r = PandasMmcif.rmsd(p1t48.df["ATOM"], p1t49.df["ATOM"], s="c-alpha", invert=False)
    assert r == 0.4923, r


def test_rna_and_nonmatching_indices():
    ehz = PandasMmcif().read_mmcif(TESTDATA_rna)
    at = ehz.df["ATOM"]
    a64 = at[at["auth_seq_id"] == 64]
    a66 = at[at["auth_seq_id"] == 66]
    r = PandasMmcif.rmsd(a64, a66)
    assert r == 10.2007, r


# def test_ligand():
#    r = PandasMmcif.rmsd(pl1.df["HETATM"], pl2.df["HETATM"], s="hydrogen", invert=True)
#    assert r == 1.9959, r


# def test_ligand_default():
#    r = PandasMmcif.rmsd(pl1.df["HETATM"], pl2.df["HETATM"], s=None)
#    assert r == 2.6444, r

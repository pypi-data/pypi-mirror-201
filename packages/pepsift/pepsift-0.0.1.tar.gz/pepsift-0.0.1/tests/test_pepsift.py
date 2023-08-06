# -*- coding: utf-8 -*-

"""Tests for Descriptor."""


import os
import unittest
import itertools

from rdkit.Chem import AllChem

from pepsift import PepSift, SiftLevel
from pepsift.utils import d_amino_acids, natural_amino_acids
from tests.constants import *


class TestPepSift(unittest.TestCase):
    """Tests for standardizer."""

    def setUp(self) -> None:
        """Load amino acids."""
        self.l_amino_acids = natural_amino_acids()
        self.d_amino_acids = d_amino_acids()
        self.natural_aa_coupling = AllChem.ReactionFromSmarts(
            '[N:1][C:2][CX3:3](=[O:4])O.[NX3:5]([H:9])([H])[C:6][C:7](=[O:8])>>[N:1][C:2][CX3:3](=[O:4])[NX3:5]([H:9])[C:6][C:7](=[O:8])')
        self.beta_homo_aa_coupling = AllChem.ReactionFromSmarts(
            '[N:1][C:2][C:3][C:4](=[O:5])O.[NH2:6][C:7][C:8][C:9](=[O:10])>>[N:1][C:2][C:3][C:4](=[O:5])[NH1:6][C:7][C:8][C:9](=[O:10])')
        self.beta_homo_natural_aa_coupling = AllChem.ReactionFromSmarts(
            '[N:1][C:2][C:3][C:4](=[O:5])O.[NH2:6][C:7][C:8](=[O:9])>>[N:1][C:2][C:3][C:4](=[O:5])[NH1:6][C:7][C:8](=[O:9])')
        self.natural_beta_homo_aa_coupling = AllChem.ReactionFromSmarts(
            '[N:1][C:2][C:3](=[O:4])O.[NH2:5][C:6][C:7][C:8](=[O:9])>>[N:1][C:2][C:3](=[O:4])[N:5][C:6][C:7][C:8](=[O:9])')
        self.alpha_methyl_aa_coupling = AllChem.ReactionFromSmarts(
            '[N:1][C:2][C:3](=[O:4])O.[NH1:5][C:6][C:7][C:8](=[O:9])>>[N:1][C:2][C:3](=[O:4])[NX3:5][C:6][C:7][C:8](=[O:9])')
        self.natural_alpha_methyl_aa_coupling = AllChem.ReactionFromSmarts(
            '[NH2:1][C:2][C:3](=[O:4])O.[NH1:5][C:6][C:7][C:8](=[O:9])>>[N:1][C:2][C:3](=[O:4])[NX3:5][C:6][C:7][C:8](=[O:9])')
        self.alpha_methyl_natural_aa_coupling = AllChem.ReactionFromSmarts(
            '[NH1:1][C:2][C:3](=[O:4])O.[NH2:5][C:6][C:7][C:8](=[O:9])>>[N:1][C:2][C:3](=[O:4])[NX3:5][C:6][C:7][C:8](=[O:9])')
        self.beta_homo_alpha_methyl_aa_coupling = AllChem.ReactionFromSmarts(
            '[NH2:1][C:2][C:3](=[O:4])O.[NH1:5][C:6][C:7][C:8](=[O:9])>>[N:1][C:2][C:3](=[O:4])[NX3:5][C:6][C:7][C:8](=[O:9])')
        self.alpha_methyl_beta_homo_aa_coupling = AllChem.ReactionFromSmarts(
            '[NH1:1][C:2][C:3](=[O:4])O.[NH2:5][C:6][C:7][C:8](=[O:9])>>[N:1][C:2][C:3](=[O:4])[NX3:5][C:6][C:7][C:8](=[O:9])')

    def test_pepsift_natural_aa(self):
        for aa_name, aa in self.l_amino_acids.items():
            print(aa_name)
            self.assertTrue(all(PepSift(level).is_peptide(aa) for level in SiftLevel))

    def test_pepsift_L_dipeptides(self):
        for (aa1_name, aa1), (aa2_name, aa2) in itertools.combinations_with_replacement(self.l_amino_acids.items(), 2):
            products = self.natural_aa_coupling.RunReactants([aa1, aa2])
            if len(products):
                for product in products:
                    print(aa1_name, aa2_name, Chem.MolToSmiles(product[0]))
                    print([PepSift(level).is_peptide(product[0]) for level in SiftLevel])
                    self.assertTrue(all(PepSift(level).is_peptide(product[0]) for level in SiftLevel))

    def test_pepsift_D_aa(self):
        for aa_name, aa in self.d_amino_acids.items():
            if aa_name != 'Gly':
                print(aa_name)
                self.assertEqual([PepSift(level).is_peptide(aa) for level in SiftLevel],
                                 [False, True, True, True, True])

    def test_pepsift_D_dipeptides(self):
        for (aa1_name, aa1), (aa2_name, aa2) in itertools.combinations_with_replacement(self.d_amino_acids.items(), 2):
            if aa1_name == 'Gly' and aa2_name == 'Gly':
                continue
            products = self.natural_aa_coupling.RunReactants([aa1, aa2])
            if len(products):
                for product in products:
                    print(aa1_name, aa2_name, Chem.MolToSmiles(product[0]))
                    print([PepSift(level).is_peptide(product[0]) for level in SiftLevel])
                    self.assertEqual([PepSift(level).is_peptide(product) for level in SiftLevel],
                                     [False, True, True, True, True])

    def test_beta_homo_aa(self):
        for aa_name, aa in LBHOMO_AA.items():
            print(aa_name)
            self.assertEqual([PepSift(level).is_peptide(aa) for level in SiftLevel],
                             [False, False, False, True, True])

    def test_pepsift_beta_homo_dipeptides(self):
        for (aa1_name, aa1), (aa2_name, aa2) in itertools.combinations_with_replacement(LBHOMO_AA.items(), 2):
            products = self.beta_homo_aa_coupling.RunReactants([aa1, aa2])
            if len(products):
                for product in products:
                    print(aa1_name, aa2_name, Chem.MolToSmiles(product[0]))
                    self.assertEqual([PepSift(level).is_peptide(product) for level in SiftLevel],
                                     [False, False, False, True, True])

    def test_pepsift_natural_beta_homo_dipeptides(self):
        for (aa1_name, aa1), (aa2_name, aa2) in itertools.product(STANDARD_AA.items(), LBHOMO_AA.items()):
            products = self.natural_beta_homo_aa_coupling.RunReactants([aa1, aa2])
            if len(products):
                for product in products:
                    print(aa1_name, aa2_name, Chem.MolToSmiles(product[0]))
                    self.assertEqual([PepSift(level).is_peptide(product) for level in SiftLevel],
                                     [False, False, True, True, True])

    def test_pepsift_beta_homo_natural_dipeptides(self):
        for (aa1_name, aa1), (aa2_name, aa2) in itertools.product(LBHOMO_AA.items(), STANDARD_AA.items()):
            products = self.natural_beta_homo_aa_coupling.RunReactants([aa1, aa2])
            if len(products):
                for product in products:
                    print(aa1_name, aa2_name, Chem.MolToSmiles(product[0]))
                    self.assertEqual([PepSift(level).is_peptide(product) for level in SiftLevel],
                                     [False, False, True, True, True])

    def test_alpha_methyl_aa(self):
        for aa_name, aa in AMHETYL_AA.items():
            print(aa_name)
            self.assertEqual([PepSift(level).is_peptide(aa) for level in SiftLevel],
                             [False, False, False, True, True])

    def test_alpha_methyl_dipeptides(self):
        for (aa1_name, aa1), (aa2_name, aa2) in itertools.combinations_with_replacement(AMHETYL_AA.items(), 2):
            products = self.alpha_methyl_aa_coupling.RunReactants([aa1, aa2])
            if len(products):
                for product in products:
                    print(aa1_name, aa2_name, Chem.MolToSmiles(product[0]))
                    self.assertEqual([PepSift(level).is_peptide(product) for level in SiftLevel],
                                     [False, False, False, True, True])

    def test_natural_alpha_methyl_dipeptides(self):
        for (aa1_name, aa1), (aa2_name, aa2) in itertools.product(AMHETYL_AA.items(), STANDARD_AA.items()):
            products = self.natural_alpha_methyl_aa_coupling.RunReactants([aa1, aa2])
            if len(products):
                for product in products:
                    print(aa1_name, aa2_name, Chem.MolToSmiles(product[0]))
                    self.assertEqual([PepSift(level).is_peptide(product) for level in SiftLevel],
                                     [False, False, True, True, True])

    def test_alpha_methyl_natural_dipeptides(self):
        for (aa1_name, aa1), (aa2_name, aa2) in itertools.product(STANDARD_AA.items(), AMHETYL_AA.items()):
            products = self.alpha_methyl_natural_aa_coupling.RunReactants([aa1, aa2])
            if len(products):
                for product in products:
                    print(aa1_name, aa2_name, Chem.MolToSmiles(product[0]))
                    self.assertEqual([PepSift(level).is_peptide(product) for level in SiftLevel],
                                     [False, False, True, True, True])

    def test_beta_homo_alpha_methyl_dipeptides(self):
        for (aa1_name, aa1), (aa2_name, aa2) in itertools.product(LBHOMO_AA.items(), AMHETYL_AA.items()):
            products = self.natural_alpha_methyl_aa_coupling.RunReactants([aa1, aa2])
            if len(products):
                for product in products:
                    print(aa1_name, aa2_name, Chem.MolToSmiles(product[0]))
                    self.assertEqual([PepSift(level).is_peptide(product) for level in SiftLevel],
                                     [False, False, False, True, True])

    def test_alpha_methyl_beta_homo_dipeptides(self):
        for (aa1_name, aa1), (aa2_name, aa2) in itertools.product(AMHETYL_AA.items(), LBHOMO_AA.items()):
            products = self.alpha_methyl_natural_aa_coupling.RunReactants([aa1, aa2])
            if len(products):
                for product in products:
                    print(aa1_name, aa2_name, Chem.MolToSmiles(product[0]))
                    self.assertEqual([PepSift(level).is_peptide(product) for level in SiftLevel],
                                     [False, False, False, True, True])

    def test_loose_amino_acid(self):
        self.assertEqual([PepSift(level).is_peptide(MOLECULES['5N1NAPHT']) for level in SiftLevel],
                         [False, False, False, False, True])

    def test_not_amino_acid(self):
        self.assertEqual([PepSift(level).is_peptide(MOLECULES['NAPHT']) for level in SiftLevel],
                         [False, False, False, False, False])
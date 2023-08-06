# -*- coding: utf-8 -*-

from __future__ import annotations
from enum import Enum, auto
from typing import List, Union
from itertools import chain

from rdkit import Chem
from rdkit.rdBase import BlockLogs
from rdkit.Chem import AllChem

from .utils import natural_amino_acids


# Backbone of amino acid SMARTS
AA_SMARTS = "[N;X3H2,X4H3+1,X2H0-1,X3r5][CX4;$([H1][*]),$([H2])][CX3](=[OX1])[O,N]"
# Backbone of beta-homo amino acid SMARTS
BH_AA_SMARTS = "[N;X3H2,X4H3+1,X2H0-1,X3r5][C][CX4;$([H1][*]),$([H2])][CX3](=[OX1])[O,N]"
# Backbone of alpha-methyl amino acid SMARTS
AM_AA_SMARTS = "[N;X3H2,X4H3+1,X2H0-1,X3r5][CX4](C)([*])[CX3](=[OX1])[O,N]"
# Carboxylic acid SMARTS
CARBOXYLIC_SMARTS = "[OX2H,OX1-][CX3]=[OX1]"
# Amine SMARTS
AMINE_SMARTS = "[N;X3H2,X3H1,X4H0+1;!$(C=O)]"
# Peptide bond SMARTS
PEPBOND_SMARTS = "[CX3](=O)[NX3;H1,r5]"
# Peptide bond splitting SMIRKS
PEPBOND_SMIRKS = "[CX3:1](=[O:2])[NX3;H1,r5:3]>>[C:1](=[O:2])O.[N:3]"

class SiftLevel(Enum):
    NaturalLAminoAcids = auto()
    NaturalLDAminoAcids = auto()
    NaturalAminoAcidDerivatives = auto()
    NonNaturalAminoAcidDerivatives = auto()
    AllAmineAndAcid = auto()


class PepSift:
    """Peptide sift allowing the identification of polymers of amino acids."""

    def __init__(self, level: SiftLevel):
        """Create a sift with custom level.

        :param level: Level of the sift: (i) NaturalLAminoAcids: identify only substructures of natural L amino acids;
        (ii) NaturalLDAminoAcids: identify only substructures of both natural L and D amino acids;
        (iii) NaturalAminoAcidDerivatives: identify general substructures of amino acids;
        (iv) NonNaturalAminoAcidDerivatives: identify also beta-homo, alpha-methyl and derived amino acids;
        (v) AllAmineAndAcid: identify anything containing both amino and carboxylic acid groups.
        """
        self.level = level

    @classmethod
    def _contains_peptide_bond(cls, mol: Chem.Mol) -> bool:
        """Determine if the molecule contains a peptide bond."""
        mol = Chem.Mol(mol)
        mol.UpdatePropertyCache()
        _ = Chem.GetSymmSSSR(mol)
        pep_bond = Chem.MolFromSmarts(PEPBOND_SMARTS)
        return mol.HasSubstructMatch(pep_bond)

    @classmethod
    def _split_along_peptide_bond(cls, mol: Chem.Mol) -> Chem.Mol:
        """Split the molecule along the peptide bonds.

        :param mol: RDKit molecule
        :return: mixture of fragments
        """
        rxn = AllChem.ReactionFromSmarts(PEPBOND_SMIRKS)
        # Copy molecule
        mol = Chem.Mol(mol)
        # Run reaction
        while cls._contains_peptide_bond(mol):
            mol.UpdatePropertyCache()
            _ = Chem.GetSymmSSSR(mol)
            prods = rxn.RunReactants((mol,))[0]
            for prod in prods:
                prod.UpdatePropertyCache()
                _ = Chem.GetSymmSSSR(prod)
            mol = AllChem.CombineMols(*prods)
            Chem.SanitizeMol(mol)
        return mol

    @classmethod
    def _neutralize(cls, mol: Chem.Mol):
        """Neutralize a molecule by adding or removing atoms.

        Adapted by Vincent Scalfani to the RDKit from Noel O’Boyle’s nocharge code.

        :param mol: RDKit molecule
        :return: the neutralized molecule
        """
        # Define SMARTS pattern
        pattern = Chem.MolFromSmarts("[+1!h0!$([*]~[-1,-2,-3,-4]),-1!$([*]~[+1,+2,+3,+4])]")
        at_matches = mol.GetSubstructMatches(pattern)
        at_matches_list = [y[0] for y in at_matches]
        if len(at_matches_list) > 0:
            for at_idx in at_matches_list:
                atom = mol.GetAtomWithIdx(at_idx)
                chg = atom.GetFormalCharge()
                hcount = atom.GetTotalNumHs()
                atom.SetFormalCharge(0)
                atom.SetNumExplicitHs(hcount - chg)
                atom.UpdatePropertyCache()
        return mol

    @classmethod
    def _remove_natural_amino_acids(cls, mol: Chem.Mol, stereo: bool = True, sanitize: bool = True) -> Chem.Mol:
        """Remove substructures in the molecule matching that of the 20 natural amino acids.

        :param mol: RDKit molecule
        :param stereo: True to consider only L-amino acids, otherwise both D and L-amino acids
        :param sanitize: should the resulting molecule be sanitized
        :return: the molecule with substructures removed
        """
        block = BlockLogs()
        # Copy & uncharge molecule
        mol = Chem.Mol(mol)
        mol = cls._neutralize(mol)
        # Split peptide bonds
        mol = cls._split_along_peptide_bond(mol)
        # Get natural amino acid
        mols = natural_amino_acids().values()
        # Carry out iterative removal of substructures
        for aa_mol in mols:
            aa_mol = Chem.AddHs(aa_mol)
            if not mol.HasSubstructMatch(aa_mol, useChirality=stereo):
                continue
            # Get unique matching atoms
            matches = sorted(set(chain.from_iterable(mol.GetSubstructMatches(aa_mol, useChirality=stereo))),
                             reverse=True)
            # Remove matching atoms
            mol = Chem.RWMol(mol)
            for idx in matches:
                mol.RemoveAtom(idx)
            mol = Chem.Mol(mol)
        # Remove isolated hydrogens
        params = Chem.RemoveHsParameters()
        params.removeDegreeZero = True
        params.removeDummyNeighbors = True
        params.removeHigherDegrees = True
        params.removeIsotopes = True
        params.removeWithQuery = True
        params.showWarnings = False
        mol = Chem.RemoveHs(mol, params)
        if sanitize:
            _ = Chem.SanitizeMol(mol)
        del block
        return mol

    @classmethod
    def _remove_natural_amino_acids_derivatives(cls, mol: Chem.Mol, sanitize: bool = True) -> Chem.Mol:
        """Remove substructures in the molecule matching that of the extended structure of amino acids.

        :param mol: RDKit molecule
        :param sanitize: should the resulting molecule be sanitized
        :return: the molecule with substructures removed
        """
        block = BlockLogs()
        # Copy molecule
        mol = Chem.Mol(mol)
        mol = Chem.AddHs(mol)
        # Sanitize mol
        mol.UpdatePropertyCache()
        _ = Chem.GetSymmSSSR(mol)
        # Uncharge molecule
        mol = cls._neutralize(mol)
        # Split peptide bonds
        mol = cls._split_along_peptide_bond(mol)
        # Carry out iterative removal of substructures
        sub_mol = Chem.MolFromSmarts(AA_SMARTS)
        # Sanitize SMARTS (not done by default)
        sub_mol.UpdatePropertyCache()
        _ = Chem.GetSymmSSSR(sub_mol)
        if not mol.HasSubstructMatch(sub_mol):
            return Chem.Mol(mol)
        # Get unique matching atoms
        matches = sorted(set(chain.from_iterable(mol.GetSubstructMatches(sub_mol))),
                         reverse=True)
        # Remove matching atoms
        mol = Chem.RWMol(mol)
        for idx in matches:
            mol.RemoveAtom(idx)
        mol = Chem.Mol(mol)
        # Remove isolated hydrogens
        params = Chem.RemoveHsParameters()
        params.removeDegreeZero = True
        params.removeDummyNeighbors = True
        params.removeHigherDegrees = True
        params.removeIsotopes = True
        params.removeWithQuery = True
        params.showWarnings = False
        mol = Chem.RemoveHs(mol, params)
        if sanitize:
            _ = Chem.SanitizeMol(mol)
        del block
        return mol

    @classmethod
    def _remove_non_natural_derivatives(cls, mol: Chem.Mol, sanitize: bool = True) -> Chem.Mol:
        """Remove substructures in the molecule matching that of the general substructure of amino acids.

        :param mol: RDKit molecule
        :param sanitize: should the resulting molecule be sanitized
        :return: the molecule with substructures removed
        """
        block = BlockLogs()
        # Copy & uncharge molecule
        mol = Chem.Mol(mol)
        mol = cls._neutralize(mol)
        # Split peptide bonds
        mol = cls._split_along_peptide_bond(mol)
        # Carry out iterative removal of substructures
        for smarts in [AA_SMARTS, BH_AA_SMARTS, AM_AA_SMARTS]:
            sub_mol = Chem.MolFromSmarts(smarts)
            # Sanitize SMARTS (not done by default)
            # and mol (not done if not first round)
            sub_mol.UpdatePropertyCache()
            _ = Chem.GetSymmSSSR(sub_mol)
            _ = Chem.GetSymmSSSR(mol)
            # Skip if no match
            if not mol.HasSubstructMatch(sub_mol):
                continue
            # Get unique matching atoms
            matches = sorted(set(chain.from_iterable(mol.GetSubstructMatches(sub_mol))),
                             reverse=True)
            # Remove matching atoms
            mol = Chem.RWMol(mol)
            for idx in matches:
                mol.RemoveAtom(idx)
            mol = Chem.Mol(mol)
        # Remove isolated hydrogens
        params = Chem.RemoveHsParameters()
        params.removeDegreeZero = True
        params.removeDummyNeighbors = True
        params.removeHigherDegrees = True
        params.removeIsotopes = True
        params.removeWithQuery = True
        params.showWarnings = False
        mol = Chem.RemoveHs(mol, params)
        if sanitize:
            _ = Chem.SanitizeMol(mol)
        del block
        return mol

    @classmethod
    def _is_loose_amino_acid(cls, mol: Chem.Mol) -> bool:
        """Check if the molecule contains both an amine and a carboxylic acid group.

        :param mol: RDKit molecule
        :return: True if the molecule can be loosely classified as an amino acid.
        """
        mol = Chem.Mol(mol)
        mol.UpdatePropertyCache()
        return mol.HasSubstructMatch(Chem.MolFromSmarts(CARBOXYLIC_SMARTS)) or \
            mol.HasSubstructMatch(Chem.MolFromSmarts(AMINE_SMARTS))

    def is_peptide(self, mol: Union[Chem.Mol, List[Chem.Mol]]):
        """Determine if the molecule(s) is/are  peptides according to the defined level.

        :param mol: RDKit molecule(s)
        :return: A boolean or list of booleans defining if each molecule is a peptide or not
        """
        # Ensure is a list
        if isinstance(mol, Chem.Mol):
            mol = [mol]
        res = []
        # Iterate molecules
        for mol_ in mol:
            mol_.UpdatePropertyCache()
            _ = Chem.GetSymmSSSR(mol_)
            mol_ = Chem.AddHs(mol_)
            # Determine strategy based on level
            if self.level is SiftLevel.NaturalLAminoAcids:
                mol_stripped = self._remove_natural_amino_acids(mol_)
                res.append(mol_stripped.GetNumHeavyAtoms() == 0)
            elif self.level is SiftLevel.NaturalLDAminoAcids:
                mol_stripped = self._remove_natural_amino_acids(mol_, stereo=False)
                res.append(mol_stripped.GetNumHeavyAtoms() == 0)
            elif self.level is SiftLevel.NaturalAminoAcidDerivatives:
                mol_stripped = self._remove_natural_amino_acids_derivatives(mol_)
                res.append(mol_.GetNumHeavyAtoms() > mol_stripped.GetNumHeavyAtoms())
            elif self.level is SiftLevel.NonNaturalAminoAcidDerivatives:
                mol_stripped = self._remove_non_natural_derivatives(mol_)
                res.append(mol_.GetNumHeavyAtoms() > mol_stripped.GetNumHeavyAtoms())
            elif self.level is SiftLevel.AllAmineAndAcid:
                res.append(self._is_loose_amino_acid(mol_))
            else:
                raise NotImplementedError(f'the specified level ({self.level}) is not implemented')
        if len(res) == 1:
            return res[0]
        return res

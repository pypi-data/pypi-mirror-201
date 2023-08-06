# -*- coding: utf-8 -*-

import os
from typing import OrderedDict
from collections import OrderedDict as ODict

import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors


def natural_amino_acids() -> OrderedDict[str, Chem.Mol]:
    # Load SMILES of natural amino acid
    json_path = os.path.join(os.path.dirname(__file__), 'natural-aa.json')
    data = pd.read_json(json_path, orient='index')
    # mols = data['SMILES'].apply(Chem.MolFromSmiles).apply(Chem.AddHs).tolist()
    mols = data['SMILES'].apply(Chem.MolFromSmiles).tolist()
    mols = ODict(sorted(zip(data.index, mols),
                        key= lambda x: Descriptors.MolWt(x[1]),
                        reverse=True))
    return mols

def d_amino_acids() -> OrderedDict[str, Chem.Mol]:
    # Load SMILES of natural amino acid
    json_path = os.path.join(os.path.dirname(__file__), 'natural-aa.json')
    data = pd.read_json(json_path, orient='index')
    # mols = data['SMILES'].apply(Chem.MolFromSmiles).apply(Chem.AddHs).tolist()
    mols = data['SMILES'].apply(Chem.MolFromSmiles).tolist()
    for mol in mols:
        for atom in mol.GetAtoms():
            if atom.GetChiralTag() is AllChem.CHI_TETRAHEDRAL_CW:
                atom.SetChiralTag(AllChem.CHI_TETRAHEDRAL_CCW)
            elif atom.GetChiralTag() is AllChem.CHI_TETRAHEDRAL_CCW:
                atom.SetChiralTag(AllChem.CHI_TETRAHEDRAL_CW)
    mols = ODict(sorted(zip(data.index, mols),
                        key= lambda x: Descriptors.MolWt(x[1]),
                        reverse=True))
    return mols

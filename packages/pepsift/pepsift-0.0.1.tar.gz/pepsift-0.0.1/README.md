# PepSift


## Summary

***Identify peptides and their derivatives from small molecule datasets.***

## Installation

```commandline
pip install pepsift
```

## Usage

First instantiate a `PepSift` by defining a level of filtering.

There are currently 5 different levels available:

| level                                      | description                                                       | comment                                                                                                                                                                             |
|--------------------------------------------|-------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `SiftLevel.NaturalLAminoAcids`             | natural L-amino acids and peptides thereof                        | e.g. identify L-Alanine or the sequence `ACDEFGHIKLMNPQRSTVWY` <br/><img src="images/L-Ala.png" alt="L-Ala" width=200>                                                              |
| `SiftLevel.NaturalLDAminoAcids`            | natural L- and D-amino acid and peptides thereof                  | e.g. identify L-Alanine or the sequences `D-A L-W`, `L-H D-Q`,   `D-M D-K` <br/><img src="images/D-Ala.png" alt="D-Ala" width=200>                                                  |
| `SiftLevel.NaturalAminoAcidDerivatives`    | derivatives of natural L- and D-amino acid and peptides   thereof | i.e. any compound containing a canonical amino acid/peptide backbone <br/><img src="images/AA.png" alt="AA" width=200>                                                              |
| `SiftLevel.NonNaturalAminoAcidDerivatives` | non-natural amino acid derivatives and peptides thereof           | e.g. identify beta-homo-alanine or alpha-methyl-Tyr <br/><img src="images/beta-homo-Ala.png" alt="BH-Ala" width=200> <img src="images/alpha-methyl-Tyr.png" alt="AM-Tyr" width=200> |
| `SiftLevel.AllAmineAndAcid`                | compounds containing amine and carboxylic acid moeities           | e.g. 3-[3-(2-Aminoethyl)cyclohexyl]propionic acid <br/><img src="images/5N1NAPHT.png" alt="5N1NAPHT" width=200>                                                                     |

These levels allow for granular selection of different types amino acids/peptides.

<br/>
Let's instantiate a sift for each level to see the difference:

```python
from pepsift import PepSift, SiftLevel

from rdkit import Chem

ps1 = PepSift(SiftLevel.NaturalLAminoAcids)
ps2 = PepSift(SiftLevel.NaturalLDAminoAcids)
ps3 = PepSift(SiftLevel.NaturalAminoAcidDerivatives)
ps4 = PepSift(SiftLevel.NonNaturalAminoAcidDerivatives)
ps5 = PepSift(SiftLevel.AllAmineAndAcid)

mols = [Chem.MolFromSmiles('C[C@@H](C(=O)O)N'),  # L-Ala
        Chem.MolFromSmiles('C[C@H](C(=O)O)N'),   # D-Ala
        Chem.MolFromSmiles('C[C@@H](CN)C(=O)O'), # Beta-homo-Ala
        Chem.MolFromSmiles('CC(C)(C(=O)O)N'),    # Alpha-methyl-Ala
        Chem.MolFromSmiles('NCCCCCCCCCCCCCCCC(=O)O'),   # Amino-hexadecanoic acid
        Chem.MolFromSmiles('c1cccc1'),           # Benzene
       ]

for mol in mols:
    print((ps1.is_peptide(mol),
           ps2.is_peptide(mol),
           ps3.is_peptide(mol),
           ps4.is_peptide(mol),
           ps5.is_peptide(mol)
           )
          )

# L-Ala
# (True, True, True, True, True)
# D-Ala
# (False, True, True, True, True)
# Beta-homo-Ala
# (False, False, True, True, True)
# Alpha-methyl-Ala
# (False, False, False, True, True)
# Amino-hexadecanoic acid
# (False, False, False, False, True)
# Benzene
# (False, False, False, False, False)
```

:warning: Any peptide containing a natural amino acid is considered a derivative of natural amino acids (even if it also contains non natural amino acids)

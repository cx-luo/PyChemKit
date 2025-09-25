# -*- coding: utf-8 -*-
# @Time    : 2025/5/13 10:36
# @Author  : chengxiang.luo
# @Email   : chengxiang.luo@pharmaron.com
# @File    : molecule.py
# @Software: PyCharm
import re

from rdkit import Chem
from rdkit.Chem.Crippen import MolLogP
from rdkit.Chem.Descriptors import MolWt, ExactMolWt
from rdkit.Chem.Lipinski import NumRotatableBonds, HeavyAtomCount, NumHAcceptors, NumHDonors
from rdkit.Chem.MolSurf import TPSA


class Molecule:
    """
    A class to represent a molecule using RDKit.

    Attributes:
        mol (Chem.Mol): RDKit molecule object
        formula (str): Molecular formula of the molecule
    """

    def __init__(self, identifier, identifier_type='smiles'):
        """
        Initialize molecule from SMILES, InChI, or formula.

        Args:
            identifier (str): The molecular identifier (e.g., 'CCO', 'C2H6O')
            identifier_type (str): Type of identifier ('smiles', 'inchi', or 'formula')
        """
        self.mol = None
        self.formula = None

        if identifier_type == 'smiles':
            self.mol = Chem.MolFromSmiles(identifier)
            if self.mol:
                self.formula = self._mol_to_formula(self.mol)
        elif identifier_type == 'inchi':
            self.mol = Chem.MolFromInchi(identifier)
            if self.mol:
                self.formula = self._mol_to_formula(self.mol)
        elif identifier_type == 'formula':
            self.formula = identifier
            # Try to generate a molecule from formula (limited support)
            # You may need to use external databases for accurate parsing
        else:
            raise ValueError("Unsupported identifier_type. Use 'smiles', 'inchi', or 'formula'.")

        if not self.mol and identifier_type != 'formula':
            raise ValueError("Invalid molecular input. Could not parse.")

    def _mol_to_formula(self, mol):
        """Generate molecular formula from RDKit Mol object."""
        formula_dict = {}
        for atom in mol.GetAtoms():
            symbol = atom.GetSymbol()
            formula_dict[symbol] = formula_dict.get(symbol, 0) + 1
        return self._dict_to_formula(formula_dict)

    def _dict_to_formula(self, element_counts):
        """Convert dictionary of elements to formula string."""
        elements = sorted(element_counts.items())
        formula = ''
        for elem, count in elements:
            formula += elem
            if count > 1:
                formula += str(count)
        return formula

    def get_formula(self):
        """Return molecular formula."""
        return self.formula

    def parse_formula(self):
        """Parse formula string into element counts."""
        pattern = r'([A-Z][a-z]*)(\d*)'
        matches = re.findall(pattern, self.formula)
        result = {}
        for elem, count in matches:
            result[elem] = int(count) if count else 1
        return result


    def get_canonical_smiles(self):
        """Return canonical SMILES string."""
        if self.mol:
            return Chem.MolToSmiles(self.mol)
        return None

    def get_inchi(self):
        """Return InChI representation."""
        if self.mol:
            return Chem.MolToInchi(self.mol)
        return None

    def get_logp(self):
        """Calculate octanol-water partition coefficient (LogP)."""
        if self.mol:
            return MolLogP(self.mol)
        return None

    def get_num_atoms(self):
        """Return number of atoms."""
        if self.mol:
            return self.mol.GetNumAtoms()
        return sum(self.parse_formula().values())

    def get_num_bonds(self):
        """Return number of bonds."""
        if self.mol:
            return self.mol.GetNumBonds()
        return None  # Cannot determine without structural info

    def get_descriptors(self):
        """Return common molecular descriptors."""
        if not self.mol:
            return {}

        return {
            "Molecular Weight": ExactMolWt(self.mol),
            "LogP": MolLogP(self.mol),
            "TPSA": TPSA(self.mol),
            "Num H Donors": NumHDonors(self.mol),
            "Num H Acceptors": NumHAcceptors(self.mol),
            "Num Rotatable Bonds": NumRotatableBonds(self.mol),
            "Num Heavy Atoms": HeavyAtomCount(self.mol)
        }

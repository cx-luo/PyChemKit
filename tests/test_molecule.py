# -*- coding: utf-8 -*-
# @Time    : 2025/5/13 10:41
# @Author  : chengxiang.luo
# @Email   : chengxiang.luo@pharmaron.com
# @File    : test_molecule.py
# @Software: PyCharm
import unittest
from molecule import Molecule


class TestMolecule(unittest.TestCase):
    def test_simple_molecule(self):
        mol = Molecule("H2O")
        self.assertEqual(mol.elements, {'H': 2, 'O': 1})
        self.assertAlmostEqual(mol.molecular_weight(), 18.0153, places=4)
        percent_composition = mol.element_percent_composition()
        self.assertAlmostEqual(percent_composition['H'], 11.19, places=2)
        self.assertAlmostEqual(percent_composition['O'], 88.81, places=2)

    def test_complex_molecule(self):
        mol = Molecule("C6H12O6")  # Glucose
        self.assertEqual(mol.elements, {'C': 6, 'H': 12, 'O': 6})
        self.assertAlmostEqual(mol.molecular_weight(), 180.156, places=3)
        percent_composition = mol.element_percent_composition()
        self.assertAlmostEqual(percent_composition['C'], 40.00, places=2)
        self.assertAlmostEqual(percent_composition['H'], 6.72, places=2)
        self.assertAlmostEqual(percent_composition['O'], 53.28, places=2)

    def test_parentheses_handling(self):
        mol = Molecule("Fe(NO3)3")
        self.assertEqual(mol.elements, {'Fe': 1, 'N': 3, 'O': 9})
        self.assertAlmostEqual(mol.molecular_weight(), 241.857, places=3)
        percent_composition = mol.element_percent_composition()
        self.assertAlmostEqual(percent_composition['Fe'], 23.93, places=2)
        self.assertAlmostEqual(percent_composition['N'], 17.37, places=2)
        self.assertAlmostEqual(percent_composition['O'], 58.70, places=2)

    def test_invalid_formula(self):
        with self.assertRaises(ValueError):
            Molecule("XyZ")


if __name__ == '__main__':
    unittest.main()

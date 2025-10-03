# -*- coding: utf-8 -*-
# @Time    : 2025/9/25 11:25
# @Author  : chengxiang.luo
# @Email   : chengxiang.luo@foxmail.com
# @File    : rxn_analysis.py
# @Software: PyCharm
from pprint import pprint
from typing import Any

from indigo import Indigo, IndigoObject
from indigo import inchi

_indigo = Indigo()
_inchi = inchi.IndigoInchi(_indigo)


class Reactant:
    def __init__(self, obj: IndigoObject, role):
        self.hash = obj.hash()
        self.cml = obj.cml()
        self.molecularWeight = round(obj.molecularWeight(), 3)
        self.monoisotopicMass = round(obj.monoisotopicMass(), 3)
        self.mostAbundantMass = round(obj.mostAbundantMass(), 3)
        self.canonicalSmiles = obj.canonicalSmiles()
        _indigo.setOption("smiles-saving-format", "daylight")
        self.smiles = obj.smiles()
        _indigo.setOption("smiles-saving-format", "chemaxon")
        self.cxSmiles = obj.smiles()
        self.isChiral = obj.isChiral()
        self.formula = obj.grossFormula().replace(' ', '', -1)
        self.inChI = _inchi.getInchi(obj)
        self.inChiKey = _inchi.getInchiKey(self.inChI)
        self.role = role
        self.stereoCentersCnt = obj.countStereocenters()


def rxn_analysis(rxn_str) -> dict[str, str | list[dict[str, Any]]]:
    rxn = _indigo.loadReaction(rxn_str)

    # Collect SMILES and other formats efficiently
    _indigo.setOption("smiles-saving-format", "daylight")
    rxn_smiles = rxn.smiles()
    _indigo.setOption("smiles-saving-format", "chemaxon")
    rxn_cx_smiles = rxn.smiles()

    result = {
        "smiles": rxn_smiles,
        "cxSmiles": rxn_cx_smiles,
        "rxnCml": rxn.cml(),
        "rxnCdXml": rxn.cdxml(),
    }

    # Helper to convert IndigoObject lists to Reactant dicts
    def _to_dicts(objs, role):
        return [Reactant(obj, role).__dict__ for obj in objs]

    result["reactants"] = _to_dicts(rxn.iterateReactants(), "reactant")
    result["products"] = _to_dicts(rxn.iterateProducts(), "product")
    result["reagents"] = _to_dicts(rxn.iterateCatalysts(), "reagent")

    return result


def rxn_serialize(rxn_str) -> dict[str, str]:
    """
    Serialize a reaction string into various formats using Indigo.
    Combines reactants and catalysts as reactants, then adds products.
    Returns canonical SMILES, unmapped/mapped SMILES, CXSMILES, and CDXML.
    """
    rxn = _indigo.loadReaction(rxn_str)
    # Collect all reactants and catalysts in one go
    reactants = list(rxn.iterateReactants())
    catalysts = list(rxn.iterateCatalysts())
    products = list(rxn.iterateProducts())

    new_rxn = _indigo.createReaction()
    for mol in (*reactants, *catalysts):
        new_rxn.addReactant(mol)
    for mol in products:
        new_rxn.addProduct(mol)

    # Unmapped
    new_rxn.automap('clear')
    _indigo.setOption("smiles-saving-format", "daylight")
    rxn_smiles = new_rxn.smiles()
    # rxn_canonical_smiles = new_rxn.canonicalSmiles()

    _indigo.setOption("smiles-saving-format", "chemaxon")
    rxn_cx_smiles = new_rxn.smiles()
    rxn_cd_xml = new_rxn.cdxml()

    # Mapped
    new_rxn.automap('alter')
    mapped_smiles = new_rxn.smiles()

    return {
        # "canonicalSmiles": rxn_canonical_smiles,
        "smiles": rxn_smiles,
        "cxSmiles": rxn_cx_smiles,
        "rxnCdXml": rxn_cd_xml,
        "mappedSmiles": mapped_smiles
    }


def rxn_canonicalize(rxn_str, sort_key="lex"):
    """
    Canonicalize a single reaction:
      - clear atom mapping
      - move agents -> reactants
      - canonicalize each molecule
      - sort reactants and products by SMILES or InChIKey
      - return both SMILES and CXSMILES
    """

    rxn = _indigo.loadReaction(rxn_str)
    rxn.automap("clear")

    # Collect reactants + agents
    reactants = [r for r in rxn.iterateReactants()] + [a for a in rxn.iterateCatalysts()]
    products = [p for p in rxn.iterateProducts()]

    # Precompute canonical SMILES and InChIKeys once
    def prep_mols(mol_list):
        mol_info = []
        for mol in mol_list:
            smi = mol.canonicalSmiles()
            inchi_key = _inchi.getInchiKey(mol) if sort_key == "inchikey" else None
            mol_info.append((smi, inchi_key))
        return mol_info

    reactant_info = prep_mols(reactants)
    product_info = prep_mols(products)
    product_cnt = len(products)

    # Sorting
    def sort_info(info):
        if sort_key == "inchikey":
            return sorted(info, key=lambda x: (x[1], x[0]))  # tie-break with SMILES
        else:
            return sorted(info, key=lambda x: x[0])

    reactant_info = sort_info(reactant_info)
    product_info = sort_info(product_info)

    # Build new reaction
    new_rxn = _indigo.createReaction()
    for smi, _ in reactant_info:
        new_rxn.addReactant(_indigo.loadMolecule(smi))
    for smi, _ in product_info:
        new_rxn.addProduct(_indigo.loadMolecule(smi))

    # Export
    _indigo.setOption("smiles-saving-format", "chemaxon")
    rxn_cx_smiles = new_rxn.smiles()

    _indigo.setOption("smiles-saving-format", "daylight")
    rxn_daylight_smiles = new_rxn.smiles()

    rxn_hash = new_rxn.hash()
    _indigo.resetOptions()

    return {"smiles": rxn_daylight_smiles, "cxSmiles": rxn_cx_smiles, "productCnt": product_cnt, "rxnHash": rxn_hash}


def rxn_uniquify(rxn_smiles):
    # This function takes a reaction string, loads it as an Indigo reaction object,
    # and then processes the reactants: A>B>C --> A.B>C
    rxn = _indigo.loadReaction(rxn_smiles)
    rxn_products = rxn.iterateProducts()
    rxn_molecules = rxn.iterateMolecules()
    products_d = [p for p in rxn_products]
    molecules_d = [m for m in rxn_molecules]

    while len(products_d) > 0:
        products_hash = [p.hash() for p in products_d]
        for i, hash_str in enumerate(products_hash):
            for j, molecule in enumerate(molecules_d):
                if molecule.hash() == hash_str:
                    products_d.pop(i)
                    molecules_d.pop(j)
                    continue

    new_rxn = _indigo.createReaction()
    _indigo.setOption("smiles-saving-format", "chemaxon")

    for reactant in molecules_d:
        new_rxn.addReactant(reactant)

    rxn_products = rxn.iterateProducts()

    for product in rxn_products:
        new_rxn.addProduct(product)

    _indigo.setOption("smiles-saving-format", "chemaxon")
    rxn_cx_smiles = new_rxn.smiles()

    rxn_cd_xml = new_rxn.cdxml()

    return {"cxSmiles": rxn_cx_smiles, "rxnCdXml": rxn_cd_xml}


if __name__ == '__main__':
    r = rxn_analysis(
        "[CH2:1]([S:3]([CH2:6][C:7]1[C:16](C(OC)=O)=[N+:15]([O-:21])[C:14]2[C:9](=[CH:10][CH:11]=[CH:12][CH:13]=2)[N+:8]=1[O-:22])(=["
        "O:5])=[O:4])[CH3:2]>[OH-].[Na+]>[CH2:1]([S:3]([CH2:6][C:7]1[CH:16]=[N+:15]([O-:21])[C:14]2[C:9](=[CH:10][CH:11]=[CH:12]["
        "CH:13]=2)[N+:8]=1[O-:22])(=[O:5])=[O:4])[CH3:2] |f:1.2|")
    pprint(r)
    d = rxn_serialize(
        "[CH2:1](O)[C:2]1[CH:7]=[CH:6][CH:5]=[CH:4][CH:3]=1.[CH3:9][N:10](C)[CH3:11]>[C]=O>[CH2:1]([N:10]([CH3:11])[CH3:9])[C:2]1[CH:7]=[CH:6][CH:5]=[CH:4][CH:3]=1 |^3:12|")

    pprint(d, width=120)

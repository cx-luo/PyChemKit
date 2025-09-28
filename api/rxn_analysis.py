# -*- coding: utf-8 -*-
# @Time    : 2025/9/25 11:25
# @Author  : chengxiang.luo
# @Email   : chengxiang.luo@foxmail.com
# @File    : rxn_analysis.py
# @Software: PyCharm

from indigo import Indigo, IndigoObject
from indigo import inchi

_indigo = Indigo()
_inchi = inchi.IndigoInchi(_indigo)


class Reactant:
    def __init__(self, obj: IndigoObject, role):
        self.hash = obj.hash()
        self.cml = obj.cml()
        self.mw = round(obj.molecularWeight(), 3)
        self.monoisotopicMass = round(obj.monoisotopicMass(), 3)
        self.mostAbundantMass = round(obj.mostAbundantMass(), 3)
        self.canonicalSmiles = obj.canonicalSmiles()
        _indigo.setOption("smiles-saving-format", "daylight")
        self.smiles = obj.smiles()
        _indigo.setOption("smiles-saving-format", "chemaxon")
        self.cxsmiles = obj.smiles()
        self.isChiral = obj.isChiral()
        self.formula = obj.grossFormula().replace(' ', '', -1)
        self.inChI = _inchi.getInchi(obj)
        self.inChiKey = _inchi.getInchiKey(self.inChI)
        self.role = role
        self.stereoCentersCnt = obj.countStereocenters()


def rxn_analysis(rxn_str):
    rxn = _indigo.loadReaction(rxn_str)
    _indigo.setOption("smiles-saving-format", "daylight")
    rxn_smiles = rxn.smiles()
    _indigo.setOption("smiles-saving-format", "chemaxon")
    rxn_cxsmiles = rxn.smiles()
    rxn_canonical_smiles = rxn.canonicalSmiles()
    rxn_cd_xml = rxn.cdxml()
    rxn_cml = rxn.cml()
    rxn_reactants = rxn.iterateReactants()
    rxn_products = rxn.iterateProducts()
    rxn_molecules = rxn.iterateMolecules()
    reactants_d = []
    products_d = []
    reagents_d = []
    for reactant in rxn_reactants:
        reactants_d.append(Reactant(reactant, 'reactant').__dict__)

    for product in rxn_products:
        products_d.append(Reactant(product, 'product').__dict__)

    for molecule in rxn_molecules:
        reagents_d.append(Reactant(molecule, 'reagent').__dict__)

    reagents_d = [p for p in reagents_d if p['inChiKey'] not in {r['inChiKey'] for r in reactants_d + products_d}]

    return {"rxnCanonicalSmiles": rxn_canonical_smiles, "smiles": rxn_smiles, "cxsmiles": rxn_cxsmiles, "rxnCml": rxn_cml,
            "rxnCdXml": rxn_cd_xml, "reactants": reactants_d, "products": products_d, "reagents": reagents_d}


def rxn_serialize(rxn_str):
    rxn = _indigo.loadReaction(rxn_str)
    rxn_products = rxn.iterateProducts()
    rxn_molecules = rxn.iterateMolecules()
    products_d = [p for p in rxn_products]
    molecules_d = [m for m in rxn_molecules]

    while len(products_d) > 0:
        products_hash = [p.hash() for p in products_d]
        for i, hash in enumerate(products_hash):
            for j, molecule in enumerate(molecules_d):
                if molecule.hash() == hash:
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

    rxn_canonical_smiles = new_rxn.canonicalSmiles()

    _indigo.setOption("smiles-saving-format", "daylight")
    rxn_smiles = new_rxn.smiles()

    _indigo.setOption("smiles-saving-format", "chemaxon")
    rxn_cxsmiles = new_rxn.smiles()

    return {"rxnCanonicalSmiles": rxn_canonical_smiles, "smiles": rxn_smiles, "cxsmiles": rxn_cxsmiles}


if __name__ == '__main__':
    r = rxn_analysis(
        "[CH2:1]([S:3]([CH2:6][C:7]1[C:16](C(OC)=O)=[N+:15]([O-:21])[C:14]2[C:9](=[CH:10][CH:11]=[CH:12][CH:13]=2)[N+:8]=1[O-:22])(=["
        "O:5])=[O:4])[CH3:2]>[OH-].[Na+]>[CH2:1]([S:3]([CH2:6][C:7]1[CH:16]=[N+:15]([O-:21])[C:14]2[C:9](=[CH:10][CH:11]=[CH:12]["
        "CH:13]=2)[N+:8]=1[O-:22])(=[O:5])=[O:4])[CH3:2] |f:1.2|")

    print(r['rxnCanonicalSmiles'])
    print(r['smiles'])
    print(r['cxsmiles'])
    d = rxn_serialize(
        "[CH2:1]([S:3]([CH2:6][C:7]1[C:16](C(OC)=O)=[N+:15]([O-:21])[C:14]2[C:9](=[CH:10][CH:11]=[CH:12][CH:13]=2)[N+:8]=1[O-:22])(=["
        "O:5])=[O:4])[CH3:2]>[OH-].[Na+]>[CH2:1]([S:3]([CH2:6][C:7]1[CH:16]=[N+:15]([O-:21])[C:14]2[C:9](=[CH:10][CH:11]=[CH:12]["
        "CH:13]=2)[N+:8]=1[O-:22])(=[O:5])=[O:4])[CH3:2] |f:1.2|")

    print(d['cxsmiles'])

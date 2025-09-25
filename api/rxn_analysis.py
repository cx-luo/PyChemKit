# -*- coding: utf-8 -*-
# @Time    : 2025/9/25 11:25
# @Author  : chengxiang.luo
# @Email   : chengxiang.luo@foxmail.com
# @File    : rxn_analysis.py
# @Software: PyCharm
from fastapi import FastAPI
from indigo import Indigo, IndigoObject
from indigo import inchi

app = FastAPI()
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
        self.smiles = obj.smiles()
        self.isChiral = obj.isChiral()
        self.formula = obj.grossFormula().replace(' ', '', -1)
        self.inChI = _inchi.getInchi(obj)
        self.inChiKey = _inchi.getInchiKey(self.inChI)
        self.role = role
        self.stereoCentersCnt = obj.countStereocenters()


def rxn_analysis(rxn_smiles):
    rxn = _indigo.loadReaction(rxn_smiles)
    rxn_smiles = rxn.smiles()
    rxn_canonical_smiles = rxn.canonicalSmiles()
    rxn_cd_xml = rxn.cdxml()
    rxn_cml = rxn.cml()
    reactants = rxn.iterateReactants()
    products = rxn.iterateProducts()
    reactants_d = []
    products_d = []
    for reactant in reactants:
        reactants_d.append(Reactant(reactant, 'reactant').__dict__)

    for product in products:
        products_d.append(Reactant(product, 'product').__dict__)

    return {"rxnCanonicalSmiles": rxn_canonical_smiles, "smiles": rxn_smiles, "rxnCml": rxn_cml, "rxnCdXml": rxn_cd_xml,
            "reactants": reactants_d, "products": products_d}

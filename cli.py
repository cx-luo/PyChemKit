# -*- coding: utf-8 -*-
# @Time    : 2025/5/13 10:37
# @Author  : chengxiang.luo
# @Email   : chengxiang.luo@pharmaron.com
# @File    : cli.py
# @Software: PyCharm
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pubchempy as pcp
from api.rxn_analysis import rxn_analysis, rxn_serialize, rxn_canonicalize, rxn_uniquify

app = FastAPI()


class Reaction(BaseModel):
    smiles: str


@app.post("/api/rxn/analysis")
async def analysis(reaction: Reaction):
    try:
        result = rxn_analysis(reaction.smiles)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing reaction: {e}")


@app.post("/api/rxn/serialize")
async def serialize(reaction: Reaction):
    try:
        result = rxn_serialize(reaction.smiles)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing reaction: {e}")


@app.post("/api/rxn/canonicalize")
async def canonicalize(reaction: Reaction):
    try:
        result = rxn_canonicalize(reaction.smiles)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing reaction: {e}")


@app.post("/api/rxn/uniquify")
async def uniquify(reaction: Reaction):
    try:
        result = rxn_uniquify(reaction.smiles)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error parsing reaction: {e}")


class ReagentName(BaseModel):
    reagent_name: str


class ReagentCid(BaseModel):
    cid: int


@app.post("/api/get/cid")
def get_cid_from_name(reagent: ReagentName):
    r_dict = {"total": 0, "cid": []}
    try:
        cids = pcp.get_cids(reagent.reagent_name, 'name')
        r_dict.update({"total": len(cids), "cid": cids})
    except Exception:
        r_dict.update({"total": 0})
    return r_dict


@app.post("/api/get/iupac")
def get_cid_from_name(reagent: ReagentCid):
    r_dict = {"total": 0, "iupac": []}
    try:
        comps = pcp.get_compounds(reagent.cid, 'cid')
        r_dict.update({"total": len(comps), "iupac": [comp.iupac_name for comp in comps]})
    except Exception as e:
        r_dict.update({"total": -1, "err": e})
    return r_dict


@app.post("/api/get/compound")
def get_compound_from_cid(reagent: ReagentCid):
    r_dict = {"total": 0, }
    try:
        comps = pcp.get_compounds(reagent.cid, 'cid')
        for comp in comps:
            r_dict.update({"total": len(comps),
                           "cid": comp.cid,
                           "mw": comp.molecular_weight,
                           # "polararea":
                           "complexity": comp.complexity,
                           "xlogp": comp.xlogp,
                           # "exactmass",
                           "monoisotopicmass": comp.monoisotopic_mass,
                           "heavycnt": comp.heavy_atom_count,
                           "hbonddonor": comp.h_bond_donor_count,
                           "hbondacc": comp.h_bond_acceptor_count,
                           "rotbonds": comp.rotatable_bond_count,
                           # "annothitcnt",
                           "charge": comp.charge, "covalentunitcnt": comp.covalent_unit_count,
                           "isotopeatomcnt": comp.isotope_atom_count, "totalatomstereocnt": comp.atom_stereo_count,
                           "definedatomstereocnt": comp.defined_atom_stereo_count,
                           'undefinedatomstereocnt': comp.undefined_atom_stereo_count,
                           'totalbondstereocnt': comp.bond_stereo_count,
                           "definedbondstereocnt": comp.defined_bond_stereo_count,
                           "undefinedbondstereocnt": comp.undefined_bond_stereo_count,
                           # "pclidcnt":,
                           # "gpidcnt":,
                           # "gpfamilycnt",
                           "aids": comp.aids,
                           # "cmpdname":comp.,
                           "inchi": comp.inchi,
                           "inchikey": comp.inchikey,
                           "isosmiles": comp.isomeric_smiles,
                           "iupacname": comp.iupac_name,
                           "mf": comp.molecular_formula,
                           "sidsrcname": comp.sids,
                           # "cidcdate",
                           # "depcatg":,
                           # "annothits": comp.,
                           # "neighbortype":,
                           "canonicalsmiles": comp.canonical_smiles})
    except Exception as e:
        r_dict.update({"total": -1, "err": e})
    return r_dict


@app.post("/api/get/cidbysmiles")
def get_cid_from_name(reagent: ReagentName):
    r_dict = {"total": 0, "cid": []}
    try:
        cids = pcp.get_cids(reagent.reagent_name, 'smiles')
        r_dict.update({"total": len(cids), "cid": cids})
    except Exception:
        r_dict.update({"total": 0})
    return r_dict


if __name__ == "__main__":
    uvicorn.run(app='cli:app', host="0.0.0.0", port=6030, reload=True)

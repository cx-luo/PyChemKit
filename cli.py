# -*- coding: utf-8 -*-
# @Time    : 2025/5/13 10:37
# @Author  : chengxiang.luo
# @Email   : chengxiang.luo@pharmaron.com
# @File    : cli.py
# @Software: PyCharm
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from api.rxn_analysis import rxn_analysis, rxn_serialize, rxn_canonicalize

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


if __name__ == "__main__":
    uvicorn.run(app='cli:app', host="0.0.0.0", port=6030, reload=True)
    # get_density_from_chemical_book('96-49-1')
    # print(get_info_from_chemical_book('1,3-dioxolan-2-one'))
    # From SMILES
    # mol1 = Molecule('CCO')  # Ethanol
    # print("Formula:", mol1.get_formula())
    # print("LogP:", mol1.get_logp())
    # print("Canonical SMILES:", mol1.get_canonical_smiles())
    # print("Descriptors:", mol1.get_descriptors())
    #
    # # From Formula
    # mol2 = Molecule('C2H6O', identifier_type='formula')
    # print("\nFormula:", mol2.get_formula())
    # print("Parsed Composition:", mol2.parse_formula())

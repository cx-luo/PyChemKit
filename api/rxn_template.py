# -*- coding: utf-8 -*-
# @Time    : 2023/9/28 10:59
# @Author  : chengxiang.luo
# @Email   : chengxiang.luo@foxmail.com
# @File    : rxn_analysis.py
# @Software: PyCharm
from pprint import pprint

from indigo import Indigo, inchi

_indigo = Indigo()
_inchi = inchi.IndigoInchi(_indigo)


def rxn_get_template(rxn_str, template_type="smarts"):
    """
    Extract reaction template from a reaction string using EPAM Indigo.

    Args:
        rxn_str (str): Reaction string in SMILES, RXN, or other supported format
        template_type (str): Type of template to extract. Options:
            - "smarts": SMARTS reaction template (default)
            - "smiles": SMILES reaction template
            - "rgroup": R-group decomposition template
            - "mapped": Mapped reaction template with atom mapping

    Returns:
        dict: Dictionary containing template information:
            - "template": The extracted template string
            - "template_type": The type of template
            - "reactant_count": Number of reactants
            - "product_count": Number of products
            - "mapping_info": Information about atom mapping (if applicable)
    """
    try:
        rxn = _indigo.loadReaction(rxn_str)

        # Get basic reaction info
        reactant_count = len(list(rxn.iterateReactants()))
        product_count = len(list(rxn.iterateProducts()))

        result = {
            "template_type": template_type,
            "reactant_count": reactant_count,
            "product_count": product_count,
            "mapping_info": {}
        }

        if template_type == "smarts":
            # Generate SMARTS template
            rxn.automap("clear")  # Clear existing mapping
            rxn.automap("discard")  # Discard mapping
            template = rxn.smarts()
            result["template"] = template

        elif template_type == "smiles":
            # Generate SMILES template (unmapped)
            rxn.automap("clear")
            _indigo.setOption("smiles-saving-format", "daylight")
            template = rxn.smiles()
            result["template"] = template

        elif template_type == "mapped":
            # Generate mapped reaction template
            rxn.automap("alter")  # Generate atom mapping
            _indigo.setOption("smiles-saving-format", "daylight")
            template = rxn.smiles()
            result["template"] = template

            # Get mapping information
            mapping_info = {
                "has_mapping": True,
                "mapped_atoms": []
            }

            # Extract mapped atoms from reactants
            for mol in rxn.iterateReactants():
                for atom in mol.iterateAtoms():
                    if rxn.atomMappingNumber(atom) > 0:
                        mapping_info["mapped_atoms"].append({
                            "atom_index": atom.index(),
                            "mapping_number": rxn.atomMappingNumber(atom),
                            "role": "reactant"
                        })

            # Extract mapped atoms from products
            for mol in rxn.iterateProducts():
                for atom in mol.iterateAtoms():
                    if rxn.atomMappingNumber(atom) > 0:
                        mapping_info["mapped_atoms"].append({
                            "atom_index": atom.index(),
                            "mapping_number": rxn.atomMappingNumber(atom),
                            "role": "product"
                        })

            result["mapping_info"] = mapping_info

        elif template_type == "rgroup":
            # Generate R-group decomposition template
            rxn.automap("clear")
            rxn.automap("discard")

            # Create R-group template by replacing side chains with R-groups
            template_rxn = _indigo.createReaction()

            # Process reactants
            for mol in rxn.iterateReactants():
                # Create a copy and simplify to R-group template
                mol_copy = mol.clone()
                # This is a simplified approach - in practice, you might want more sophisticated R-group detection
                template_rxn.addReactant(mol_copy)

            # Process products
            for mol in rxn.iterateProducts():
                mol_copy = mol.clone()
                template_rxn.addProduct(mol_copy)

            _indigo.setOption("smiles-saving-format", "daylight")
            template = template_rxn.smiles()
            result["template"] = template

        else:
            raise ValueError(f"Unsupported template type: {template_type}")

        return result

    except Exception as e:
        return {
            "error": f"Failed to extract template: {str(e)}",
            "template_type": template_type,
            "template": None
        }


def rxn_compare_templates(rxn1_str, rxn2_str, template_type="smarts"):
    """
    Compare two reactions using their templates.

    Args:
        rxn1_str (str): First reaction string
        rxn2_str (str): Second reaction string
        template_type (str): Type of template to use for comparison

    Returns:
        dict: Comparison results including similarity and template information
    """
    try:
        # Extract templates
        template1 = rxn_get_template(rxn1_str, template_type)
        template2 = rxn_get_template(rxn2_str, template_type)

        if "error" in template1 or "error" in template2:
            return {
                "error": "Failed to extract templates from one or both reactions",
                "template1": template1,
                "template2": template2
            }

        # Load reactions for comparison
        rxn1 = _indigo.loadReaction(rxn1_str)
        rxn2 = _indigo.loadReaction(rxn2_str)

        # Calculate similarity using Indigo's built-in similarity
        similarity = rxn1.similarity(rxn2, "tanimoto")

        # Check if templates are identical
        templates_identical = template1["template"] == template2["template"]

        return {
            "similarity": similarity,
            "templates_identical": templates_identical,
            "template1": template1,
            "template2": template2,
            "comparison_type": template_type
        }

    except Exception as e:
        return {
            "error": f"Failed to compare reactions: {str(e)}",
            "template1": None,
            "template2": None
        }


def rxn_template_statistics(template_str, template_type="smarts"):
    """
    Analyze a reaction template and provide statistical information.

    Args:
        template_str (str): Template string to analyze
        template_type (str): Type of template (smarts, smiles, etc.)

    Returns:
        dict: Statistical information about the template
    """
    try:
        if template_type == "smarts":
            rxn = _indigo.loadReactionSmarts(template_str)
        else:
            rxn = _indigo.loadReaction(template_str)

        # Count atoms and bonds
        total_atoms = 0
        total_bonds = 0
        reactant_atoms = 0
        product_atoms = 0

        for mol in rxn.iterateReactants():
            total_atoms += mol.countAtoms()
            total_bonds += mol.countBonds()
            reactant_atoms += mol.countAtoms()

        for mol in rxn.iterateProducts():
            total_atoms += mol.countAtoms()
            total_bonds += mol.countBonds()
            product_atoms += mol.countAtoms()

        # Count functional groups (simplified)
        functional_groups = {
            "aromatic_rings": 0,
            "aliphatic_rings": 0,
            "double_bonds": 0,
            "triple_bonds": 0
        }

        for mol in rxn.iterateMolecules():
            functional_groups["aromatic_rings"] += mol.countAromaticRings()
            functional_groups["aliphatic_rings"] += mol.countAliphaticRings()

            for bond in mol.iterateBonds():
                if bond.bondOrder() == 2:
                    functional_groups["double_bonds"] += 1
                elif bond.bondOrder() == 3:
                    functional_groups["triple_bonds"] += 1

        return {
            "template_type": template_type,
            "total_atoms": total_atoms,
            "total_bonds": total_bonds,
            "reactant_atoms": reactant_atoms,
            "product_atoms": product_atoms,
            "functional_groups": functional_groups,
            "reactant_count": len(list(rxn.iterateReactants())),
            "product_count": len(list(rxn.iterateProducts())),
            "template_complexity": total_atoms + total_bonds  # Simple complexity metric
        }

    except Exception as e:
        return {
            "error": f"Failed to analyze template: {str(e)}",
            "template_type": template_type
        }


if __name__ == '__main__':
    # Test reaction template extraction
    print("\n=== Reaction Template Extraction ===")
    test_reaction = ("[N+](C1C=CC=C2C=1C=CN=C2)([O-])=O.[CH3:14][C:15]1[C:24]2[C:19](=[CH:20][CH:21]=[CH:22][CH:23]=2)[CH:18]=[CH:17]["
                     "N:16]=1.Br.[Cl:26][C:27]1[C:32]([OH:33])=[C:31]([Cl:34])[C:30]([Cl:35])=[C:29]([Cl:36])[C:28]=1[Cl:37]>>[Cl:26]["
                     "C:27]1[C:32]([O-:33])=[C:31]([Cl:34])[C:30]([Cl:35])=[C:29]([Cl:36])[C:28]=1[Cl:37].[CH3:14][C:15]1[C:24]2[C:19](=["
                     "CH:20][CH:21]=[CH:22][CH:23]=2)[CH:18]=[CH:17][NH+:16]=1 |f:4.5|")

    # Test different template types
    for template_type in ["smarts", "smiles", "mapped", "rgroup"]:
        print(f"\n--- {template_type.upper()} Template ---")
        template_result = rxn_get_template(test_reaction, template_type)
        pprint(template_result, width=100)

    # Test template comparison
    print("\n=== Template Comparison ===")
    rxn1 = "CCO.CC(=O)O>>CC(=O)OCC"
    rxn2 = "CCO.CH3COOH>>CH3COOCH2CH3"
    comparison = rxn_compare_templates(rxn1, rxn2, "smarts")
    pprint(comparison, width=100)

    # Test template statistics
    print("\n=== Template Statistics ===")
    smarts_template = rxn_get_template(test_reaction, "smarts")["template"]
    if smarts_template:
        stats = rxn_template_statistics(smarts_template, "smarts")
        pprint(stats, width=100)

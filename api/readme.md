```python
def save_moldata(
    md, output_format=None, options={}, indigo=None, library=None
):
    if output_format in ("monomer-library", "chemical/x-monomer-library"):
        return md.struct.monomerLibrary()
    elif output_format in ("chemical/x-mdl-molfile", "chemical/x-mdl-rxnfile"):
        return md.struct.rxnfile() if md.is_rxn else md.struct.molfile()
    elif output_format == "chemical/x-indigo-ket":
        return md.struct.json()
    elif output_format == "chemical/x-sequence":
        return md.struct.sequence(library)
    elif output_format == "chemical/x-peptide-sequence-3-letter":
        return md.struct.sequence3Letter(library)
    elif output_format == "chemical/x-fasta":
        return md.struct.fasta(library)
    elif output_format == "chemical/x-idt":
        return md.struct.idt(library)
    elif output_format == "chemical/x-helm":
        return md.struct.helm(library)
    elif output_format == "chemical/x-daylight-smiles":
        if options.get("smiles") == "canonical":
            return md.struct.canonicalSmiles()
        else:
            indigo.setOption("smiles-saving-format", "daylight")
            return md.struct.smiles()
    elif output_format == "chemical/x-chemaxon-cxsmiles":
        if options.get("smiles") == "canonical":
            return md.struct.canonicalSmiles()
        else:
            indigo.setOption("smiles-saving-format", "chemaxon")
            return md.struct.smiles()
    elif output_format == "chemical/x-daylight-smarts":
        return md.struct.smarts()
    elif output_format == "chemical/x-cml":
        return md.struct.cml()
    elif output_format == "chemical/x-cdxml":
        return md.struct.cdxml()
    elif output_format == "chemical/x-cdx":
        return md.struct.b64cdx()
    elif output_format == "chemical/x-inchi":
        return indigo.inchi.getInchi(md.struct)
    elif output_format == "chemical/x-inchi-key":
        return indigo.inchi.getInchiKey(indigo.inchi.getInchi(md.struct))
    elif output_format == "chemical/x-inchi-aux":
        res = indigo.inchi.getInchi(md.struct)
        aux = indigo.inchi.getAuxInfo()
        return "{}\n{}".format(res, aux)
    elif output_format == "chemical/x-sdf":
        buffer = indigo.writeBuffer()
        sdfSaver = indigo.createSaver(buffer, "sdf")
        for frag in md.struct.iterateComponents():
            sdfSaver.append(frag.clone())
        sdfSaver.close()
        return buffer.toString()
    elif output_format == "chemical/x-rdf":
        buffer = indigo.writeBuffer()
        rdfSaver = indigo.createSaver(buffer, "rdf")
        for reac in md.struct.iterateReactions():
            rdfSaver.append(reac.clone())
        rdfSaver.close()
        return buffer.toString()
    raise HttpException("Format %s is not supported" % output_format, 400)

```

```python
def automap(self, mode=""):
    """Automatic reaction atom-to-atom mapping

    Args:
        mode (str): mode is one of the following (separated by a space):
        "discard" : discards the existing mapping entirely and considers
                    only the existing reaction centers (the default)
        "keep"    : keeps the existing mapping and maps unmapped atoms
        "alter"   : alters the existing mapping, and maps the rest of the
                    reaction but may change the existing mapping
        "clear"   : removes the mapping from the reaction.

        "ignore_charges" : do not consider atom charges while searching
        "ignore_isotopes" : do not consider atom isotopes while searching
        "ignore_valence" : do not consider atom valence while searching
        "ignore_radicals" : do not consider atom radicals while searching

    Returns:
        int: 1 if atom mapping is done without errors
    """
```
from pymedtermino import *
from pymedtermino.snomedct import *
from pymedtermino.meddra import *

# initialize MedDRA terminology
meddra = get_ontology("http://purl.bioontology.org/ontology/MEDDRA/")

# load MedDRA terminology
meddra.load()

# example ADE entities extracted from text using SciBERT
ade_entities = ['nausea', 'headache', 'rash']

# loop through each ADE entity and map to a MedDRA term
for ade in ade_entities:
    results = meddra.search(ade)
    if results:
        meddra_term = results[0].name
        print(f"ADE entity: {ade}, MedDRA term: {meddra_term}")
    else:
        print(f"No matching MedDRA term found for ADE entity: {ade}")

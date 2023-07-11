import requests
import os
from dotenv import load_dotenv

# Specify the path to the .env file
dotenv_path = '../.env'  # the path to my .env file

# Load the environment variables from the .env file
load_dotenv(dotenv_path)

# Retrieve the email address and API key from environment variables
email = os.getenv('UTS_EMAIL')
api_key = os.getenv('UTS_API_KEY')
base_url = "https://uts-ws.nlm.nih.gov/rest"

def map_cui_to_meddra(cui):
    # Step 1: Retrieve CUI information
    cui_url = f"{base_url}/content/current/CUI/{cui}"
    headers = {"Content-Type": "application/json"}
    params = {"ticket": api_key}
    response = requests.get(cui_url, headers=headers, params=params)
    cui_info = response.json()

    # Step 2: Search for MedDRA mappings
    meddra_mappings = []
    if "result" in cui_info:
        concept = cui_info["result"]
        if "relations" in concept:
            relations = concept["relations"]
            for relation in relations:
                if relation["relationLabel"] == "HL7/MEDDRA":
                    meddra_code = relation["relatedId"]
                    meddra_mappings.append(meddra_code)

    return meddra_mappings

def get_meddra_term(meddra_code):

    # Step 1: Retrieve MedDRA concept information
    meddra_url = f"{base_url}/content/current/MEDDRA/{meddra_code}"
    headers = {"Content-Type": "application/json"}
    params = {"ticket": api_key}
    response = requests.get(meddra_url, headers=headers, params=params)
    meddra_info = response.json()

    # Step 2: Retrieve MedDRA term
    meddra_term = None
    if "result" in meddra_info:
        concept = meddra_info["result"]
        if "name" in concept:
            meddra_term = concept["name"]

    return meddra_term

# Example usage
cui = "C0746883"  # Replace with your desired CUI
meddra_mappings = map_cui_to_meddra(cui)

if meddra_mappings:
    meddra_terms = []
    for meddra_code in meddra_mappings:
        meddra_term = get_meddra_term(meddra_code)
        if meddra_term:
            meddra_terms.append(meddra_term)
    print("MedDRA Mappings:", meddra_mappings)
    print("MedDRA Terms:", meddra_terms)
else:
    print("No MedDRA mappings found for the given CUI.")

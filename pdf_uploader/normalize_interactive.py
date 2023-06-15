import pickle
from PubMedRecord import PubMedRecord
from PubMedRecord import PubMedRecordsList
import os
from dotenv import load_dotenv
from skr_web_api import Submission, METAMAP_INTERACTIVE_URL

file_path = 'ner_out_short.pkl'

with open(file_path, 'rb') as file:
    data = pickle.load(file)

# Specify the path to the .env file
dotenv_path = '../.env'  # the path to my .env file

# Load the environment variables from the .env file
load_dotenv(dotenv_path)

# Retrieve the email address and API key from environment variables
email = os.getenv('UTS_EMAIL')
api_key = os.getenv('UTS_API_KEY')

# Populate the input_texts list with ade_entities from each record
for record in data.records:
    input_text = record.ade_entities

    # Create a MetaMap submission instance
    inst = Submission(email, api_key)
    # Set the MetaMap service URL if necessary
    service_url = METAMAP_INTERACTIVE_URL
    inst.set_serviceurl(service_url)

    inst.init_mm_interactive(input_text, args='-N')

    # Submit the request to MetaMap
    response = inst.submit()

    cuis = []
    for line in response.content.decode().split('\n'):
        if line.startswith('USER|MMI'):
            fields = line.split('|')
            if len(fields) >= 6:
                cui = fields[4]
                cuis.append(cui)

    # Print the extracted CUIs
    print('Extracted CUIs:', cuis)
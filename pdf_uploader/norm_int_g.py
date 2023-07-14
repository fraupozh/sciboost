from PubMedRecord import PubMedRecord
from PubMedRecord import PubMedRecordsList
import pickle
import time
import os
from dotenv import load_dotenv
from skr_web_api import Submission, METAMAP_INTERACTIVE_URL

# Specify the path to the .env file
dotenv_path = '../.env'  # the path to my .env file

# Load the environment variables from the .env file
load_dotenv(dotenv_path)

# Retrieve the email address and API key from environment variables
email = os.getenv('UTS_EMAIL')
api_key = os.getenv('UTS_API_KEY')

# Load the PubMedRecordsList from the pickle file
file_path = 'ner_out_short.pkl'
with open(file_path, 'rb') as file:
    data = pickle.load(file)

# Create a MetaMap submission instance
inst = Submission(email, api_key)

# Set the MetaMap service URL if necessary
service_url = METAMAP_INTERACTIVE_URL
inst.set_serviceurl(service_url)

# Process each record
for i, record in enumerate(data.records):
    input_text = record.ade_entities

    # Initialize MetaMap interactive mode with the input text
    inst.init_mm_interactive(input_text, args='-N')

    # Submit the request to MetaMap
    response = inst.submit()

    # Print the response status code and content
    #print('Response status:', response.status_code)
    #print('Response content:', response.content.decode())

    #concept_names = re.findall(r'USER\|MMI\|[\d.]+\|([^|]+)\|[A-Z]\d+', response.content.decode())
    #unique_concept_names = list(set(concept_names))

    
    # Extract the concept names from the response content
    unique_concept_names = []
    for line in response.content.decode().split('\n'):
        if line.startswith('USER|MMI'):
            fields = line.split('|')
            if len(fields) >= 6:
                name = fields[3]
                unique_concept_names.append(name)
    unique_concept_names = list(set(unique_concept_names))
    print(unique_concept_names)

    cuis = []
    for line in response.content.decode().split('\n'):
        if line.startswith('USER|MMI'):
            fields = line.split('|')
            if len(fields) >= 6:
                cui = fields[4]
                cuis.append(cui)
    print(cuis)

    # Check if it's the last record to avoid waiting before completion
    if i != len(data.records) - 1:
        # Wait for 6 seconds before processing the next record (to comply with the rate limit)
        time.sleep(6)

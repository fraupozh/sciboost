from PubMedRecord import PubMedRecord
from PubMedRecord import PubMedRecordsList
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

# Create a MetaMap submission instance
inst = Submission(email, api_key)

# Set the MetaMap service URL if necessary
service_url = METAMAP_INTERACTIVE_URL
inst.set_serviceurl(service_url)

# Retrieve all PubMedRecord objects from the database
records = PubMedRecord.objects.all()

# Process each record
for i, record in enumerate(records):
    input_text = record.ade_entities

    # Initialize MetaMap interactive mode with the input text
    inst.init_mm_interactive(input_text, args='-N')

    # Submit the request to MetaMap
    response = inst.submit()

    # Extract the concept names and CUIs from the response content
    unique_concept_names = []
    cuis = []
    for line in response.content.decode().split('\n'):
        if line.startswith('USER|MMI'):
            fields = line.split('|')
            if len(fields) >= 6:
                name = fields[3]
                cui = fields[4]
                unique_concept_names.append(name)
                cuis.append(cui)
    unique_concept_names = list(set(unique_concept_names))

    # Update the PubMedRecord object with the ade_normalized and cuis attributes
    record.ade_normalized = unique_concept_names
    record.cuis = cuis
    record.save()

    # Check if it's the last record to avoid waiting before completion
    if i != len(records) - 1:
        # Wait for 6 seconds before processing the next record (to comply with the rate limit)
        time.sleep(6)

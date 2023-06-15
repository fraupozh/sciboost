import pickle
from PubMedRecord import PubMedRecord
from PubMedRecord import PubMedRecordsList

file_path = 'ner_out.pkl'

with open(file_path, 'rb') as file:
    data = pickle.load(file)


'''there are two options to use MetaMap: Python wrapper or web API.

Wrapper: https://github.com/AnthonyMRios/pymetamap
WebAPI: https://github.com/lhncbc/skr_web_python_api
More details about WebAPI: https://lhncbc.nlm.nih.gov/ii/tools/Web_API_Access.html

'''
'''
To map the extracted ADEs to MedDRA PTs, we processed the text through MetaMap7,
 which assigns Concept Unique Identifiers (CUIs) from the Unified Medical Language
   System (UMLS) to biomedical text. From the UMLS CUI, we identify the MedDRA PT
     associated with that CUI. If one exists, we assign the MedDRA PT 
     to the mention.
'''
import os
from dotenv import load_dotenv
from skr_web_api import Submission, BATCH_VALIDATION_URL #METAMAP_INTERACTIVE_URL
import requests
# Specify the path to the .env file
dotenv_path = '../.env'  # the path to my .env file

# Load the environment variables from the .env file
load_dotenv(dotenv_path)

# Retrieve the email address and API key from environment variables
email = os.getenv('UTS_EMAIL')
api_key = os.getenv('UTS_API_KEY')

# Create a list to store the input texts
input_texts = []

# Populate the input_texts list with ade_entities from each record
for record in data.records:
    input_texts.append(record.ade_entities)

# Create a MetaMap submission instance
inst = Submission(email, api_key)

# Set the MetaMap service URL if necessary
service_url = BATCH_VALIDATION_URL #METAMAP_INTERACTIVE_URL
inst.set_serviceurl(service_url)

# Initialize MetaMap interactive mode with the input text
inst.init_generic_batch('semrep', '-D')

input_text_str = '\n\n'.join('\n'.join(record) for record in input_texts)

# Set the batch file with the input text string
batch_file_name = 'input_records'
inst.set_batch_file(batch_file_name, input_text_str)

# Submit the request to MetaMap
response = inst.submit()

# Print the response status code and content
print('Response status:', response.status_code)
print('Response content:', response.content.decode())

# Extract the job ID from the response content
job_id = None
for line in response.content.decode().split('\n'):
    if line.startswith('----- Citation'):
        job_id = line.split(' ')[2]
        break

if job_id:
    # Construct the URL to access the result files
    result_url = f"https://ii.nlm.nih.gov/Scheduler/foo/{job_id}/text.out"

    # Define the local path to save the result file
    save_path = "./text.out"

    # Wait for 5 seconds before attempting to download the result file
    time.sleep(5)

    # Download the result file
    response = requests.get(result_url)

    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            file.write(response.content)
        print('Result file downloaded successfully.')
    else:
        print('Failed to download the result file. Status code:', response.status_code)
else:
    print('Job ID not found in the response.')

    # Extract CUIs from the updated response
'''
    cuis = []
    for line in response.content.decode().split('\n'):
        if line.startswith('USER|MMI'):
            fields = line.split('|')
            if len(fields) >= 6:
                cui = fields[4]
                cuis.append(cui)

    # Print the extracted CUIs
    print('Extracted CUIs:', cuis)


# Print the response status code and content
#print('Response status:', response.status_code)
#print('Response content:', response.content.decode())
''''''
cuis = []
for line in response.content.decode().split('\n'):
    if line.startswith('USER|MMI'):
        fields = line.split('|')
        if len(fields) >= 6:
            cui = fields[4]
            cuis.append(cui)

# Print the extracted CUIs
print('Extracted CUIs:', cuis)
'''
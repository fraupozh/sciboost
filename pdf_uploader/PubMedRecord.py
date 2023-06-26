from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from Bio import Medline
from skr_web_api import Submission, METAMAP_INTERACTIVE_URL
#import time
import os
from dotenv import load_dotenv

# Specify the path to the .env file
dotenv_path = './.env'  # the path to my .env file

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

def load_ner_model():
    model_checkpoint = "jsylee/scibert_scivocab_uncased-finetuned-ner"
    ner_tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, model_max_length=512)
    ner_model = AutoModelForTokenClassification.from_pretrained(model_checkpoint, num_labels=5,
                                                            id2label={0: 'O', 1: 'B-DRUG', 2: 'I-DRUG', 3: 'B-EFFECT', 4: 'I-EFFECT'}
                                                            )        
    ner_pipeline = pipeline(task='ner', model=ner_model, tokenizer=ner_tokenizer)

    return ner_pipeline

class PubMedRecord:

    def __init__(self, record):
        #record = {key.decode('utf-8'): [value.decode('utf-8') for value in values] for key, values in record.items()}
        self.record_id = record.get('PMID')
        #print("ID:", self.record_id)
        self.article_identifier = record.get('AID', None)
        self.author = record.get('AU', None)
        self.affiliation = record.get('AD', None)
        self.title = record.get('TI', None)
        self.publication_date = record.get('DP', None)
        self.publication_type = record.get('PT', None)
        self.location_identifier = record.get('LID', None)
        self.abstract = record.get('AB', None)
        self.ner = self.process()
        self.drug_entities = self.detect_drugs()
        self.ade_entities = self.detect_ade()
        self.ade_normalized, self.cuis = self.process_ade()

    def process(self):
        ner_pipeline = load_ner_model()
        ner = ner_pipeline(self.abstract)
        return ner

    def detect_drugs(self):
        drug_entities = [{entity['word']:entity['entity']} for entity in self.ner if entity['entity'] == "B-DRUG" or entity['entity'] == "I-DRUG"]
        drug_names = ""
        for item in drug_entities:
            for word, tag in item.items():
                if tag == "B-DRUG":
                    drug_names += "DRUG-" + word
                elif tag == "I-DRUG":
                    drug_names += word.removeprefix('##')
        drug_list = drug_names.split("DRUG-")
        drug_list = list(set([d for d in drug_list if d]))  # remove any empty strings

        return drug_list
    
    def detect_ade(self):
        ade_entities = [{entity['word']:entity['entity']} for entity in self.ner if entity['entity'] == "B-EFFECT" or entity['entity'] == "I-EFFECT"]
        ade = ""
        for item in ade_entities:
            for word, tag in item.items():
                if tag == 'B-EFFECT':
                    ade += 'ADE-' + word + " "
                elif tag == 'I-EFFECT':
                    ade += word.removeprefix('##') + " "
        ade_list = ade.split("ADE-")
        ade_list = list(set([d.strip() for d in ade_list if d]))

        return ade_list
    
    def process_ade(self):
        input_text = self.ade_entities

        # Initialize MetaMap interactive mode with the input text
        inst.init_mm_interactive(input_text, args='-N')
        print("MetaMap interactive initialized with input text:", input_text)

        # Submit the request to MetaMap
        response = inst.submit()
        print("MetaMap request submitted")

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

        print("Unique Concept Names:", unique_concept_names)
        print("CUIs:", cuis)

        return unique_concept_names, cuis

    

    
    

    

class PubMedRecordsList:
    
    def __init__(self, pubmed_file):
        self.records = [PubMedRecord(record) for record in Medline.parse(pubmed_file)]
        self.list_of_unique_drugs = list(self.unique_drugs())

    def unique_drugs(self):
        unique_drugs = set()
        for record in self.records:
            if record.drug_entities is not None:
                for drug in record.drug_entities:
                    unique_drugs.add(drug)
        return unique_drugs
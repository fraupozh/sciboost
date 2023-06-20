import pickle
#from ner_model import load_ner_model
from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
from Bio import Medline

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
        self.record_id = record['PMID']
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



class PubMedRecordsList:
    
    def __init__(self, pubmed_file):
        self.records = [PubMedRecord(record) for record in Medline.parse(pubmed_file)]
        self.list_of_unique_drugs = list(self.unique_drugs())

    def unique_drugs(self):
        unique_drugs = set()
        for record in self.records:
            for drug in record.drug_entities:
                unique_drugs.add(drug)
        return unique_drugs

        

#class Drug:
    '''Users will get the heatmap based on number of articles with respect to drug names on x-axis and side effects on y-axis. The list of ADEs (ade_list) for a particular drug is 
    a summary of all ADEs that were found in abstracts where the drug was mentioned. However, when a study compares multiple drugs, 
    it's not guaranteed that every ADE listed is associated with our drug of interest. To address this issue, 
    the ML model should be trained to identify the relationship between the drug-entity and the ADE-entity.
    As of now, if an unexpected ADE is found in the context of our drug, users can easily access the Pubmed records from which the entities were extracted via clicking on the number of articles on the heatmap.'''
'''
    def __init__(self, drug_name, PubMedRecordsList):
        #self.name = drug_name
        self.records_reported_the_drug = [record for record in PubMedRecordsList if self.name in record.drug_entities]
        self.ade_list = list(set([record.ade_entities for record in self.records_reported_the_drug]))



class ADE:

    def __init__(self, ade_name, drug):
        self.ade_name = ade_name
        self.records = drug.records_reported_the_drug       
        self.list_of_records_per_ade = [record for record in drug.records_reported_the_drug if ade_name in record.ade_entities]

'''

if __name__ == "__main__":
    # Code to execute when the script is run directly
    with open("test_data_9.txt") as handle:
        records_list = PubMedRecordsList(handle)

    with open("ner_out_short.pkl", "wb") as file:
        pickle.dump(records_list, file)

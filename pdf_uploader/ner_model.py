from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification

#Load the pre-trained NER model for drug name and adverse effect detection
def load_ner_model():
    from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
    model_checkpoint = "jsylee/scibert_scivocab_uncased-finetuned-ner"
    ner_tokenizer = AutoTokenizer.from_pretrained(model_checkpoint, model_max_length=512)
    ner_model = AutoModelForTokenClassification.from_pretrained(model_checkpoint, num_labels=5,
                                                            id2label={0: 'O', 1: 'B-DRUG', 2: 'I-DRUG', 3: 'B-EFFECT', 4: 'I-EFFECT'}
                                                            )        
    ner_pipeline = pipeline(task='ner', model=ner_model, tokenizer=ner_tokenizer)

    return ner_pipeline
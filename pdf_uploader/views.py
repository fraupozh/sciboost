from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pdf_uploader.PubMedRecord import PubMedRecordM, PubMedRecordsList
from pdf_uploader.models import PubMedRecord
from django.http import JsonResponse
from .models import PubMedRecord
import os
from Bio import Medline
from django.shortcuts import get_object_or_404



"""
@csrf_exempt
def upload(request):
    if request.method == 'POST' and request.FILES['pubmed_file']:
        pubmed_file = request.FILES['pubmed_file']
        #print(pubmed_file.read())
        
        # Specify the encoding when reading the file
        decoded_content = pubmed_file.read().decode('utf-8')
        #print(decoded_content)
        pubmed_records_list = PubMedRecordsList(decoded_content)
        
        records = pubmed_records_list.records

        # Process each record and save them
        for record in records:
            record.save()

        context = {}  # Add any required data to the context dictionary
        return render(request, 'success.html', context)
    else:
        return render(request, 'upload.html')
"""

@csrf_exempt
def upload(request):
    if request.method == 'POST' and request.FILES['pubmed_file']:
        pubmed_file = request.FILES['pubmed_file']
        
        # create a list with existing record IDs in the database
        existing_record_ids = list(record.record_id for record in PubMedRecord.objects.all())
        if existing_record_ids:
            for id in existing_record_ids:
                print("Existing id:", id)
        else:
            print("Database is empty")
        
        records_list = []
        for record in Medline.parse(pubmed_file):
            if int(record.get("PMID")) not in existing_record_ids:
                pm_record = PubMedRecordM(record)
                #print("TITLE:", pm_record.title)
                records_list.append(pm_record)
            else:
                continue
        
        for record in records_list:
            pubmed_record = PubMedRecord(
                record_id=record.record_id,
                article_identifier=record.article_identifier,
                author=record.author,
                affiliation=record.affiliation,
                title=record.title,
                publication_date=record.publication_date,
                publication_type=record.publication_type,
                location_identifier=record.location_identifier,
                abstract=record.abstract,
                drug_entities=record.drug_entities,
                ade_entities=record.ade_entities,
                ade_normalized=record.ade_normalized,
                cuis=record.cuis
            )
            pubmed_record.save()

        context = {}  # Add any required data to the context dictionary
        return render(request, 'success.html', context)
    else:
        return render(request, 'upload.html')
    

def demo(request):
    # Use the pre-existing file for demo
    file_path = os.path.join(os.path.dirname(__file__), 'test_data_short.txt')
    # create a list with existing records ids in the database
    existing_record_ids = list(record.record_id for record in PubMedRecord.objects.all())
    if existing_record_ids:
        for id in existing_record_ids:
            print("Existing id:", id)
    else:
        print("Database is empty")

    records_list = []    
    with open(file_path, 'r', encoding='utf-8') as handle:
        for record in Medline.parse(handle):
            if int(record.get("PMID")) not in existing_record_ids:
                pm_record = PubMedRecordM(record)
                #print("TITLE:", pm_record.title)
                records_list.append(pm_record)
            else:
                continue

        
        for record in records_list:
            pubmed_record = PubMedRecord(
                record_id=record.record_id,
                article_identifier=record.article_identifier,
                author=record.author,
                affiliation=record.affiliation,
                title=record.title,
                publication_date=record.publication_date,
                publication_type=record.publication_type,
                location_identifier=record.location_identifier,
                abstract=record.abstract,
                drug_entities = record.drug_entities,
                ade_entities = record.ade_entities,
                ade_normalized = record.ade_normalized,
                cuis = record.cuis
            )
            pubmed_record.save()

    context = {}  # Add any required data to the context dictionary
    return render(request, 'success.html', context)


def download_json(request):
    records = PubMedRecord.objects.all()

    data = []
    for record in records:
        record_data = {
            'record_id': record.record_id,
            'article_identifier': record.article_identifier,
            'author': record.author,
            'affiliation': record.affiliation,
            'title': record.title,
            'publication_date': str(record.publication_date),
            'publication_type': record.publication_type,
            'location_identifier': record.location_identifier,
            'abstract': record.abstract,
            'drug_entities': record.drug_entities,
            'ade_entities': record.ade_entities,
            'ade_normalized': record.ade_normalized,
            'cuis': record.cuis
        }
        data.append(record_data)

    return JsonResponse(data, safe=False, content_type='application/json')

'''
def table_view(request):
    # Your view logic here
    return render(request, 'table.html')
'''
'''
from django.db.models import Q
from functools import reduce
import operator

@csrf_exempt
def custom_json(request):
    selected_drugs = request.GET.getlist('drugs[]')

    if not selected_drugs:
        # Retrieve all records if no drugs are selected
        records = PubMedRecord.objects.all()
    else:
        # Filter records based on the selected drugs
        records = PubMedRecord.objects.filter(
            reduce(
                operator.or_,
                (Q(drug_entities__contains=drug) for drug in selected_drugs)
            )
        )

    data = []
    for record in records:
        record_data = {
            'record_id': record.record_id,
            'article_identifier': record.article_identifier,
            'author': record.author,
            'affiliation': record.affiliation,
            'title': record.title,
            'publication_date': str(record.publication_date),
            'publication_type': record.publication_type,
            'location_identifier': record.location_identifier,
            'abstract': record.abstract,
            'drug_entities': record.drug_entities,
            'ade_entities': record.ade_entities,
            'ade_normalized': record.ade_normalized,
            'cuis': record.cuis
        }
        data.append(record_data)

    return JsonResponse(data, safe=False, content_type='application/json')
'''

from django.db.models import Q
from functools import reduce
import operator

def custom_json(request):
    selected_drugs = request.GET.getlist('drugs[]')

    if not selected_drugs:
        # Return an empty response if no drugs are selected
        return JsonResponse([], safe=False, content_type='application/json')
    else:
        # Filter records based on the selected drugs
        records = PubMedRecord.objects.filter(
            reduce(
                operator.or_,
                (Q(drug_entities__contains=drug) for drug in selected_drugs)
            )
        )

        data = []
        for record in records:
            record_data = {
                'record_id': record.record_id,
                'article_identifier': record.article_identifier,
                'author': record.author,
                'affiliation': record.affiliation,
                'title': record.title,
                'publication_date': str(record.publication_date),
                'publication_type': record.publication_type,
                'location_identifier': record.location_identifier,
                'abstract': record.abstract,
                'drug_entities': record.drug_entities,
                'ade_entities': record.ade_entities,
                'ade_normalized': record.ade_normalized,
                'cuis': record.cuis
            }
            data.append(record_data)

        return JsonResponse(data, safe=False, content_type='application/json')

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from pdf_uploader.PubMedRecord import PubMedRecord, PubMedRecordsList
import json
from pdf_uploader.models import PubMedRecord
from django.http import HttpResponse
import os

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
        # User uploaded a file, process it as before
        pubmed_file = request.FILES['pubmed_file']
        pubmed_records_list = PubMedRecordsList(pubmed_file)
        
        records = pubmed_records_list.records

        # Process each record and save them
        for record in records:
            record.save()

        context = {}  # Add any required data to the context dictionary
        return render(request, 'success.html', context)
    else:
        return render(request, 'upload.html')


def demo(request):
    # Use the pre-existing file for demo
    file_path = os.path.join(os.path.dirname(__file__), 'test_data_9.txt')

    with open(file_path, 'r', encoding='utf-8') as handle:
        records_list = PubMedRecordsList(handle)
        
        for record in records_list.records:
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
                ade_entities = record.ade_entities
            )
            pubmed_record.save()

    context = {}  # Add any required data to the context dictionary
    return render(request, 'success.html', context)





def generate_json(request):
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
        }
        data.append(record_data)
    
    json_data = json.dumps(data)
    
    response = HttpResponse(json_data, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="pubmed_records.json"'
    
    return response







    

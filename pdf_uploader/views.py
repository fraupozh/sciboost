# Import the required modules
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt



@csrf_exempt
def upload(request):
    if request.method == 'POST' and request.FILES['pubmed_file']:
        pubmed_file = request.FILES['pubmed_file']
        # parse Pubmed file with biopython
        abstracts = PubMedRecordList(pubmed_file)
        # Perform drug name and adverse effect detection 
        
        drug_names = [(entity['word'], entity['entity']) for entity in entities if entity['entity'] == 'DRUG']
        classifications = [(entity['word'], entity['entity']) for entity in entities if entity['entity'] == 'EFFECT']
        context = {
            'drug_names': drug_names,
            'classifications': classifications,
        }
        return render(request, 'result.html', context)
    else:
        return render(request, 'upload.html')




    

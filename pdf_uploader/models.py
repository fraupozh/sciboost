from django.db import models


class PubMedRecord(models.Model):
    record_id = models.BigIntegerField(primary_key=True)
    article_identifier = models.CharField(max_length=55)
    author = models.CharField(max_length=200)
    affiliation = models.TextField(max_length=200)
    title = models.TextField(max_length=200)
    publication_date = models.CharField(max_length=200)
    publication_type = models.CharField(max_length=200)
    location_identifier = models.CharField(max_length=200)
    abstract = models.TextField()
    drug_entities = models.CharField(max_length=200)
    ade_entities = models.CharField(max_length=200)    


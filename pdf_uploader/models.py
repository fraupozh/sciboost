from django.db import models

# Create your models here.

from django.db import models


class Drug(models.Model):
    drug_name = models.CharField(max_length=200)
    adverse_effect = models.CharField(max_length=200)    


# Generated by Django 4.1.7 on 2023-07-11 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pdf_uploader', '0002_pubmedrecord_ade_normalized_pubmedrecord_cuis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pubmedrecord',
            name='affiliation',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pubmedrecord',
            name='author',
            field=models.TextField(blank=True, null=True),
        ),
    ]
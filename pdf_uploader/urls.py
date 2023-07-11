'''
from django.urls import path
from pdf_uploader import views

app_name = 'pdf_uploader'

urlpatterns = [
    path('demo/', views.demo, name='demo'),
    path('download_json/', views.download_json, name='download_json'),
    path('', views.upload, name='upload'),
]
'''

from django.urls import path
from . import views

app_name = 'pdf_uploader'

urlpatterns = [
    path('', views.upload, name='upload'),
    path('demo/', views.demo, name='demo'),
    path('download_json/', views.download_json, name='download_json'),
    path('table/', views.table_view, name='table'),
    path('custom_json/', views.custom_json, name='custom_json'),
]

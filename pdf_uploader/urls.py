from django.urls import path

from . import views

urlpatterns = [
    path("", views.upload, name="upload"),
    path('demo/', views.demo, name='demo'),
    path("generate_json/", views.generate_json, name="generate_json"),
    #path("heatmap/", views.heatmap, name="heatmap"),
]

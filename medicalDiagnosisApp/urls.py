from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('malaria_diagnose', views.malaria_diagnose, name='malaria_diagnose'),
    path('pneumonia_diagnose', views.pneumonia_diagnose, name='pneumonia_diagnose'),

]
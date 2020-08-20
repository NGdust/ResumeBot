from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('create/employer/', views.CreateEmployer.as_view(), name='create_employer'),
    path('create/condidate/', views.CreateCondidate.as_view(), name='create_condidate'),
]
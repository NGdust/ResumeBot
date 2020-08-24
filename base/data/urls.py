from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('vacansies/', views.GetVacansies.as_view(), name='vacansies'),
    path('resumes/', views.GetResumes.as_view(), name='resumes'),
    path('create/vacansy/', views.CreateVacansy.as_view(), name='create_vacansy'),
    path('create/resume/', views.CreateResume.as_view(), name='create_resume'),
]
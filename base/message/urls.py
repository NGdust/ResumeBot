from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('faq', views.GetFAQ.as_view(), name='faq'),
]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.Leads.as_view(), name='leads'),
    path('employers/', views.Employers.as_view(), name='employers'),
    path('condidats/', views.Condidats.as_view(), name='condidats'),

    path('vacansy/<int:id>', views.VacansyView.as_view(), name='vacansy'),
    path('condidat/<int:id>', views.CondidatView.as_view(), name='condidat'),
    path('employer/<int:id>', views.EmploerView.as_view(), name='employer'),
    path('login/', views.LoginView.as_view(), name='login'),
]
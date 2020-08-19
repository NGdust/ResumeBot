from django.contrib import admin
from .models import Vacansy, Resume
# Register your models here.

@admin.register(Vacansy)
class VacansyAdmin(admin.ModelAdmin):
    list_display = ('employer', 'position', 'salary')

@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'company', 'date')

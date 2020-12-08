from django.contrib import admin

# Register your models here.
from .models import FAQ


@admin.register(FAQ)
class ResumeAdmin(admin.ModelAdmin):
    pass

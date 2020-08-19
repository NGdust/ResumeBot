from django.db import models
from user.models import Candidate, Employer

class Vacansy(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    position = models.CharField('Должность', blank=True, null=True, max_length=256)
    experience = models.CharField('Опыт', blank=True, null=True, max_length=256)
    age = models.CharField('Возраст', blank=True, null=True, max_length=256)
    description = models.CharField('Описание', blank=True, null=True, max_length=2048)
    salary = models.IntegerField('Зарплата', blank=True, null=True)


class Resume(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    company = models.CharField('Компания', blank=True, null=True, max_length=256)
    date = models.CharField('Срок работы', blank=True, null=True, max_length=256)
    reason = models.TextField('Причина увольнения', blank=True, null=True)
    results = models.TextField('Результаты', blank=True, null=True)
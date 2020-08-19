# Generated by Django 3.1 on 2020-08-19 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0003_candidate_employer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vacansy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=256, null=True, verbose_name='Должность')),
                ('experience', models.CharField(blank=True, max_length=256, null=True, verbose_name='Опыт')),
                ('age', models.CharField(blank=True, max_length=256, null=True, verbose_name='Возраст')),
                ('description', models.CharField(blank=True, max_length=2048, null=True, verbose_name='Описание')),
                ('salary', models.IntegerField(blank=True, null=True, verbose_name='Зарплата')),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.employer')),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(blank=True, max_length=256, null=True, verbose_name='Компания')),
                ('date', models.CharField(blank=True, max_length=256, null=True, verbose_name='Срок работы')),
                ('reason', models.TextField(blank=True, null=True, verbose_name='Причина увольнения')),
                ('results', models.TextField(blank=True, null=True, verbose_name='Результаты')),
                ('candidate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.candidate')),
            ],
        ),
    ]
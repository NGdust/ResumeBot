from django.shortcuts import render
from data.models import Vacansy, Resume
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Employer, Candidate
from data.models import Vacansy, Resume

def clearData(data):
    for k, v in data.items():
        try:
            data[k] = v[0]
        except TypeError:
            data[k] = v
    return data

class CreateVacansy(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = clearData({**request.data})
        username = data.pop('username')
        employer = Employer.objects.get(username=username)
        Vacansy.objects.create(employer=employer, **data)
        response = {'status': 'Done'}
        return Response(response)

class CreateResume(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = clearData({**request.data})
        username = data.pop('username')
        candidate = Candidate.objects.get(username=username)
        Resume.objects.create(candidate=candidate, **data)
        response = {'status': 'Done'}
        return Response(response)

class GetVacansies(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        username = request.query_params.get('username')
        employer = Employer.objects.get(username=username)
        vacansies = Vacansy.objects.filter(employer=employer)
        response = []
        if len(vacansies) == 0:
            return Response(response)
        for vacansy in vacansies:
            vacansyData = {
                "position": vacansy.position,
                "experience": vacansy.experience,
                "age": vacansy.age,
                "description": vacansy.description,
                "salary": vacansy.salary,
            }
            response.append(vacansyData)
        return Response(response)

class GetResumes(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        username = request.query_params.get('username')
        candidate = Candidate.objects.get(username=username)
        resumes = Resume.objects.filter(candidate=candidate)
        response = []
        if len(resumes) == 0:
            return Response(response)
        for resume in resumes:
            resumeData = {
                "company": resume.company,
                "position": resume.position,
                "experience": resume.experience,
                "reason": resume.reason,
                "results": resume.results,
            }
            response.append(resumeData)
        return Response(response)
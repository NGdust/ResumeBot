from django.shortcuts import render
from data.models import Vacansy, Resume
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView


def clearData(data):
    for k, v in data.items():
        data[k] = v[0]
    return data

class CreateVacansy(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = clearData({**request.data})

        response = {'status': 'Done'}
        return Response(response)

class CreateResume(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = clearData({**request.data})
        response = {'status': 'Done'}
        return Response(response)
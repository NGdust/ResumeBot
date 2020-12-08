from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Employer, Candidate, User


def clearData(data):
    for k, v in data.items():
        data[k] = v[0]
    return data

class CreateEmployer(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = clearData({**request.data})
        username = data.pop('username')
        email = data.pop('email')
        if not Employer.objects.filter(username=username):
            Employer.objects.create(username=username, email=email).set_password('1')
        Employer.objects.filter(username=username).update(**data)
        response = {'status': 'Done'}
        return Response(response)

class CreateCondidate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = clearData({**request.data})
        username = data.pop('username')
        email = data.pop('email')
        if not Candidate.objects.filter(username=username):
            Candidate.objects.create(username=username, email=email).set_password('1')
        Candidate.objects.filter(username=username).update(**data)
        response = {'status': 'Done'}
        return Response(response)

class DeleteUser(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        username = request.query_params.get('username')
        User.objects.get(username=username).delete()
        return Response({'status': 'Done'})
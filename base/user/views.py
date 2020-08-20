from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import Employer, Candidate


def clearData(data):
    for k, v in data.items():
        data[k] = v[0]
    return data

class CreateEmployer(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = clearData({**request.data})

        try: Employer.objects.create(username=data['username'], email=data['email']).set_password('1')
        except: pass
        Employer.objects.filter(username=data['username']).update(
                                                                    company=data['company'],
                                                                    category=data['company'],
                                                                    address=data['company'],
                                                                    fio=data['company'],
                                                                    phone=data['company'],
                                                                    url=data['company'],
                                                                    chat_id=data['chat_id'],
                                                                 )
        response = {'status': 'Done'}
        return Response(response)

class CreateCondidate(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = clearData({**request.data})
        try:Candidate.objects.create(username=data['username'], email=data['email']).set_password('1')
        except:pass
        Candidate.objects.filter(username=data['username']).update(
                                                                        name=data['name'],
                                                                        secondname=data['secondname'],
                                                                        age=data['age'],
                                                                        address=data['address'],
                                                                        phone=data['company'],
                                                                        url=data['company'],
                                                                        chat_id=data['chat_id'],
                                                                  )
        response = {'status': 'Done'}
        return Response(response)
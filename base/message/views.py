from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FAQ


class GetFAQ(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        type = request.query_params.get('type')
        try:
            faq = FAQ.objects.get(type=type)
            text = faq.text
        except FAQ.DoesNotExist:
            text = ""
        return Response({'text': text})
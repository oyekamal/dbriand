from .models import MarkQuestion
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import MarkSerializer, ConceptSerializer
from .predict import Question

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class ConceptViewSet(viewsets.ViewSet):
    agent = Question()
    def create(self, request):
        serializer = ConceptSerializer(data=request.data)
        if serializer.is_valid():
            activities = self.agent.nextQuestion(request.data)
            # Your logic here
            return Response(activities, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MarkView(viewsets.ViewSet):
    """
    A simple ViewSet for Predicting some data.
    """
    agent = Question()

    def list(self, request):
        return Response(None)

    def retrieve(self, request, pk=None):
        return Response(None)

    def post(self, request):
        payload = request.data
        activities = self.agent.nextQuestion(payload)
        return Response(activities)



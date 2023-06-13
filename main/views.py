from .models import MarkQuestion
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import MarkSerializer
from .predict import Question


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



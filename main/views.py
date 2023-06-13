from .models import MarkQuestion
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import MarkSerializer, ConceptSerializer
from .predict import Question

from rest_framework import status
from rest_framework.decorators import action


class ConceptViewSet(viewsets.ViewSet):
    agent = Question()
    def create(self, request):
        serializer = ConceptSerializer(data=request.data)
        if serializer.is_valid():
            activities = self.agent.nextQuestion(request.data)
            # Your logic here
            return Response(activities, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    @action(detail=False, methods=['get'])
    def get_question_mastery(self, request):
        concept_uid = request.query_params.get('concept_uid', None)
        if concept_uid:
            # Your logic here to get question mastery
            data = self.agent.getQuestionMastery(concept_uid)
            data = {"concept_uid": concept_uid, "mastery": "example_mastery", "data": data}
            return Response(data, status=status.HTTP_200_OK)
        return Response({"error": "concept_uid is required."}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def get_search_results(self, request):
        # Your logic here to get search results
        data = {"search_results": "example_search_results"}
        return Response(data, status=status.HTTP_200_OK)


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



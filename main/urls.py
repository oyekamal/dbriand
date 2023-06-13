from django.urls import path, include
from .views import MarkView, ConceptViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'api/v1', MarkView, basename="question_request")
router.register(r'api/v2', ConceptViewSet, basename='concept_view')
urlpatterns = [
    path('', include(router.urls)),
]

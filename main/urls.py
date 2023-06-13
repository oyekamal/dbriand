from django.urls import path, include
from .views import MarkView
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'api/v1', MarkView, basename="question_request")

urlpatterns = [
    path('', include(router.urls)),
]

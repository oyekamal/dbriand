from rest_framework import serializers
from .models import MarkQuestion


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkQuestion
        fields = ["link", "data", "response"]
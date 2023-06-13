from rest_framework import serializers
from .models import MarkQuestion
from rest_framework.serializers import ValidationError


class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkQuestion
        fields = ["link", "data", "response"]
        
        
class ConceptSerializer(serializers.Serializer):
    concept_uid = serializers.CharField(max_length=255)
    user_id = serializers.CharField(max_length=255)

    def validate(self, data):
        if not data["concept_uid"] or not data["user_id"]:
            raise ValidationError("Both concept_uid and user_id are required.")
        return data

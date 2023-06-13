from django.db import models
from jsonfield import JSONField


# Create your models here.
class MarkQuestion(models.Model):
    link = models.CharField(max_length=30)
    data = JSONField()
    response = JSONField()
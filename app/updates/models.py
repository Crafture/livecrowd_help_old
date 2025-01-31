from django.db import models
from core.models import TimeStampedModel
from clients.models import Client

class Update(TimeStampedModel):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    content = models.TextField()

    def __str__(self):
        return self.title
from django.db import models
from django.contrib.auth.models import User, Group
from core.models import TimeStampedModel


class Client(TimeStampedModel):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

    def natural_key(self):
        return self.name

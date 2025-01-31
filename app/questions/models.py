from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel
from django.dispatch import receiver
from django.db.models.signals import post_save
from events.models import Event
from clients.models import Client

DEFAULT_USER_CREATED_ID = 1


class Category(TimeStampedModel):
    # event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    category = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.category

    def natural_key(self):
        return self.category


class Question(TimeStampedModel):
    question = models.CharField(max_length=500)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True)
    answer = models.TextField(blank=True)
    info = models.TextField(blank=True)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='question_verified_by_set', null=True,
                                    blank=True)
    count = models.PositiveIntegerField(default=0)
    user_created = models.ForeignKey(User, related_name='question_user_created_set', on_delete=models.CASCADE,
                                     default=DEFAULT_USER_CREATED_ID)
    is_archived = models.BooleanField('Archived', default=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True, default=None)

    def __str__(self):
        return self.question

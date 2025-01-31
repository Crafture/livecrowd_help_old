from django.db import models
from core.models import TimeStampedModel
from clients.models import Client


class Venue(TimeStampedModel):
	venue = models.CharField(max_length=500)
	address = models.CharField(max_length=500, null=True, blank=True)
	venue_info = models.TextField(blank=True, null=True)
	client = models.ForeignKey(Client, on_delete=models.CASCADE, blank=True, null=True)

	#add production per venue
	def __str__(self):
		title = str(self.venue) + " - " + str(self.client)
		return title
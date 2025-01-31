from django.db import models
from django.contrib.auth.models import User
from core.models import TimeStampedModel
from venues.models import Venue
from django.http import JsonResponse
from django.views.generic.edit import CreateView

class AjaxableResponseMixin:
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'pk': self.object.pk,
            }
            return JsonResponse(data)
        else:
            return response


class Event(TimeStampedModel):
    event = models.CharField(max_length=500, unique=False)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    date_of_event = models.DateTimeField('Date of Event:',auto_now_add=True)
    user_created = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    event_notes = models.TextField('Notes, Details, Production Team, Phone Numbers etc.', null=True, blank=True)
    is_archived = models.BooleanField('Archived', default=False)

    def natural_key(self):
        return self.event

    def __str__(self):
        title = str(self.event) + " - " + str(self.venue)
        # if self.venue:
        #     title = str(self.event) + " - " + str(self.venue)
        # else:
        #     title = str(self.event)
        return title
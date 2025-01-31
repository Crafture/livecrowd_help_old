from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Question, Category
from events.models import Event
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget, DateTimeWidget
from django_summernote.admin import SummernoteModelAdmin
from clients.models import Client
from venues.models import Venue


# EVENT WIDGET
class EventWidget(ForeignKeyWidget):
    def __init__(
            self,
            model,
            field='pk',
            create=False,
            *args, **kwargs):
        self.model = model
        self.field = field
        self.create = create

    def clean(self, value, row=None, *args, **kwargs):
        venue_row_value = row["venue"]
        venue = Venue.objects.filter(venue__iexact=venue_row_value).first()
        obj, created = self.model.objects.get_or_create(event=value, venue=venue)
        return obj

# CLIENT WIDGET
class ClientWidget(ForeignKeyWidget):
    def __init__(
            self,
            model,
            field='pk',
            create=False,
            *args, **kwargs):
        self.model = model
        self.field = field
        self.create = create

    def clean(self, value, row=None, *args, **kwargs):
        obj, created = self.model.objects.get_or_create(name=value)
        return obj


# VENUE WIDGET
class VenueWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        client = Client.objects.get(name__iexact=row["client"])
        obj, created = self.model.objects.get_or_create(venue=value, client=client)
        return obj


class CategoryWidget(ForeignKeyWidget):
    def clean(self, value, row=None, *args, **kwargs):
        obj, created = self.model.objects.get_or_create(category=value)
        return obj


class QuestionResource(resources.ModelResource):
    client = fields.Field(
        column_name='client',
        attribute='client',
        widget=ClientWidget(Client, 'name')
    )
    category = fields.Field(
        column_name='category',
        attribute='category',
        widget=CategoryWidget(Category, 'category')
    )
    venue = fields.Field(
        column_name='venue',
        attribute='venue',
        widget=VenueWidget(Venue, 'venue')
    )
    event = fields.Field(
        column_name='event',
        attribute='event',
        widget=EventWidget(Event, 'event')
    )

    class Meta:
        model = Question
        fields = ['id', 'client', 'question', 'venue', 'category', 'answer', 'event',]


@admin.register(Question)
class QuestionAdmin(ImportExportModelAdmin, SummernoteModelAdmin):
    exclude = ('verified_by',)
    resource_class = QuestionResource
    summernote_fields = ('answer', 'info')
    # Displays the columns in the admin page overview of questions
    list_display = ('question', 'event', 'category', 'verified', 'verified_by',)
    # Immediately edit the model by clicking on the question, category or verified
    list_display_links = ('question', 'event', 'category', 'verified')

    # filtering in the adminpage:
    list_filter = ('verified', 'event', 'category',)

    def save_model(self, request, obj, form, change):
        if obj.verified == True:
            obj.verified_by = request.user
        else:
            obj.verified_by = None
        super().save_model(request, obj, form, change)


admin.site.register(Category)

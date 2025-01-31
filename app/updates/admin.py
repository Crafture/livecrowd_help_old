from django.contrib import admin
from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from django_summernote.admin import SummernoteModelAdmin
from .models import Update
from clients.models import Client


class UpdateResource(resources.ModelResource):
    event = fields.Field (
        column_name='client',
        attribute='client',
        widget=ForeignKeyWidget(Client, 'client')
    )

    class Meta:
        model = Update
        fields = '__all__'
    # exclude = ('created', 'modified', 'verified', 'count', 'user_created')


# Register your models here.
@admin.register(Update)
class UpdateAdmin(SummernoteModelAdmin):
    resource_class = UpdateResource
    summernote_fields = ('content',)
    # Displays the columns in the admin page overview of questions
    # list_display = ('question', 'event', 'category', 'verified', 'verified_by',)
    # # Immediately edit the model by clicking on the question, category or verified
    # list_display_links = ('question', 'event', 'category', 'verified')

    # filtering in the adminpage:
    # list_filter = ('verified', 'event', 'category',)

    # def save_model(self, request, obj, form, change):
    #     if obj.verified == True:
    #         obj.verified_by = request.user
    #     else:
    #         obj.verified_by = None
    #     super ().save_model (request, obj, form, change)

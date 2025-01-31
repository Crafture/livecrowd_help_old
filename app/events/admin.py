from django.contrib import admin
from .models import Event
from questions.models import Question

# Register your models here.


class QuestionInline(admin.TabularInline):
    model = Question

    def save_model(self, request, obj, form, change):
        if obj.verified == True:
            obj.verified_by = request.user
        else:
            obj.verified_by = None
            obj.verified = False

        super().save_model(request, obj, form, change)


class EventAdmin(admin.ModelAdmin):
    exclude = ("user_created",)

    # inlines = [
    # 	QuestionInline,
    # ]
    def save_model(self, request, obj, form, change):
        obj.user_created = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Event, EventAdmin)

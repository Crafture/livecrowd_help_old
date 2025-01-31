from django.core import serializers
from django.http import JsonResponse
from .models import Update


def GetUpdate(request, pk=None):
    if pk is not None:
        update = Update.objects.filter(client__pk=pk)[:1]
    else:
        if request.user.profile.client:
            update = Update.objects.filter(client__pk=request.user.profile.client.pk)[:1]
        else:
            update = Update.objects.all().order_by('-created')
    data = serializers.serialize("json", update, use_natural_foreign_keys=True)
    return JsonResponse(data, status=200, safe=False)

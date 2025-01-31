from django.urls import path, include
from .views import *
from updates.views import GetUpdate

urlpatterns = [
    # Returns Query with all client names:
    path('get/', ClientsGet, name='clients-get'),
    # Returns Query with all clients and their questions:
    path('get/all/', ClientsGetAll, name='clients-get-all'),
    path('<int:pk>/', ClientView.as_view(), name='client-view'),
    path('<int:pk>/update/', GetUpdate, name='get-client-update'),
    path('<int:pk>/get/', ClientGetQuestions, name='client-view-get'),
    path('<int:pk>/query/', ClientQuestionQueryset, name='client-question-queryset'),
    path('<int:pk>/question-create/', ClientQuestionCreate, name='client-question-create'),
    path('<int:client_id>/question-update/<int:pk>/', ClientQuestionUpdate, name='client-question-update'),
    path('<int:client_id>/question-delete/<int:pk>/', ClientDeleteQuestion, name='client-question-delete'),
    path('<int:client_id>/question-archive/<int:pk>/', ClientArchiveQuestion, name='client-question-archive'),
]
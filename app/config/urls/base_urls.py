from django.contrib import admin
from django.urls import path, include

from questions.views import *
from updates.views import GetUpdate

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('/', views.index),
    path('', IndexView.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    #path('venue-create/', VenueCreate.as_view(), name='venue-create'),
    path('update/', GetUpdate, name="get-update"),
    path('question-create/', QuestionCreate, name='question-create'),
    path('question-delete/<int:pk>/', DeleteQuestion, name='question-delete'),
    path('question-archive/<int:pk>/', ArchiveQuestion, name='question-archive'),
    path('query/', QuestionQueryset, name='question-queryset'),
    path('query/all/', AllQuestions, name='all-questions'),
    path('question-update/<int:pk>/', QuestionUpdate, name='question-update'),
    path('<int:pk>/count-plus/', CountPlus, name='count-plus'),
    path('categories-get/', CategoriesGet, name='categories-get'),
    path('events-get/', EventsGet, name='events-get'),
    path('event-info-get/', EventInfoGet, name='event-info-get'),
    #path('<str:event>/', EventView.as_view(), name='event'),
    path('summernote/', include('django_summernote.urls')),
    path('clients/', include('clients.urls')),
    path('updates/', include('updates.urls')),
]
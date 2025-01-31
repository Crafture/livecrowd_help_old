from .models import Client
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from questions.models import Question, Category
from events.models import Event
from venues.models import Venue


@login_required
def ClientsGet(request):
    """
    Get all clients if the user is a Livecrowd User.
    If not: Only present the one client tab of the user.

    :param request:
    :return:
    """
    if request.user.profile.client == None:
        queryset_clients = Client.objects.all()
    elif request.user.profile.client == 'Livecrowd':
        queryset_clients = Client.objects.all()
    else:
        client = request.user.profile.client.name
        print(str(client))
        queryset_clients = Client.objects.filter(name=client)
    data = serializers.serialize("json", queryset_clients, use_natural_foreign_keys=True)
    return JsonResponse(data, status=200, safe=False)


# @login_required
# def ClientLoad(request, pk):
#     """
#     Loads the 10 latest questions of the client.
#     :param request:
#     :return:
#     """
#     client = Client.objects.get(pk=pk)
#     print(client)
#     #data = serializers.serialize("json", queryset_clients, use_natural_foreign_keys=True)
#     #return JsonResponse(data, status=200, safe=False)

# MAIN EVENT VIEW
class ClientView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login/'
    # model = Question
    template_name = 'faq/faq.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        client = self.kwargs['pk']
        venue_list = Venue.objects.filter(client=client)
        if self.request.user.profile.client == 'Livecrowd':
            client_list = Client.objects.all()
        elif not self.request.user.profile.client:
            client_list = Client.objects.all()
        else:
            client_name = self.request.user.profile.client
            client_list = Client.objects.filter(name=client_name)

        # To pass 'active' class we need to check the url and compare it to the clients pk
        current_client = self.kwargs['pk']
        context['venue_list'] = venue_list
        context['client_list'] = client_list
        context['current_client'] = current_client
        return context

    # def get_queryset(self, **kwargs):
    #     if self.request.user.profile.client:
    #         client = self.request.user.profile.client.name
    #     else:
    #         client = Client.objects.get(pk=self.kwargs['pk'])
    #     queryset = Question.objects.filter(client__name=client)
    #
    #     data = serializers.serialize("json", queryset, use_natural_foreign_keys=True)
    #     return JsonResponse(data, status=200, safe=False)

    # def get(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     data = serializers.serialize("json", queryset, use_natural_foreign_keys=True)
    #     return JsonResponse(data, status=200, safe=False)


@login_required
def ClientsGetAll(request):
    queryset_questions = Question.objects.all().order_by('client')
    data = serializers.serialize("json", queryset_questions, use_natural_foreign_keys=True)
    return JsonRespons(data, status=200, safe=False)


@login_required
def ClientsGetEvents(request):
    if request.user.profile.client:
        if request.user.profile.client == 'Livecrowd':
            queryset_questions = Event.objects.all().filter(client=client)
        client = request.user.profile.client

    queryset_questions = Event.objects.all().filter(client=client)


@login_required
def QuestionQueryset(request):
    key_list = []
    for key in request.GET.getlist('pk'):
        key_list.append(key)

    query = Question.objects.filter(event__pk__in=key_list).filter(is_archived=False)
    print(query)
    data = serializers.serialize("json", query, use_natural_foreign_keys=True)
    return JsonResponse(data, status=200, safe=False)


@login_required
def ClientGetQuestions(request, pk):
    query = Question.objects.filter(client__pk=pk)
    data = serializers.serialize("json", query, use_natural_foreign_keys=True)
    return JsonResponse(data, status=200, safe=False)


@login_required
def ClientQuestionQueryset(request, pk):
    key_list = []

    for key in request.GET.getlist('pk'):
        key_list.append(key)

    client = Client.objects.get(pk=pk)
    query = Question.objects.filter(client__pk=client.pk, event__pk__in=key_list, is_archived=False)

    data = serializers.serialize("json", query, use_natural_foreign_keys=True)
    return JsonResponse(data, status=200, safe=False)


# QUESTION CREATE VIEW
@login_required
def ClientQuestionCreate(request, pk):
    if request.method == 'POST':
        question = request.POST['question']
        answer = request.POST['answer']
        category = Category.objects.get(category=request.POST['category'])
        event = Event.objects.get(event=request.POST['event'])
        client = Client.objects.get(pk=pk)
        # client = request.user.profile.client
        user_created = request.user
        Question.objects.create(question=question, answer=answer, category=category, event=event,
                                user_created=user_created, client=client)
        return HttpResponse("OK")
    else:
        return HttpResponse("FORM INVALID")


@login_required
def ClientQuestionUpdate(request, client_id, pk):
    if request.method == 'POST':
        query = Question.objects.get(pk=pk)
        query.question = request.POST['question']
        query.answer = request.POST['answer']
        query.user_created = request.user
        query.client = Client.objects.get(pk=client_id)
        query.save()
        return HttpResponse("OK")
    else:
        return HttpResponse("FORM INVALID")


@login_required
def ClientDeleteQuestion(request, client_id, pk):
    question = Question.objects.get(pk=pk).delete()
    return HttpResponse("OK")


@login_required
def ClientArchiveQuestion(request, client_id, pk):
    question = Question.objects.get(pk=pk)
    question.is_archived = True
    question.save()
    return HttpResponse("OK")

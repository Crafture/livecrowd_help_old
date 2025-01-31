from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from questions.models import Question, Category
from events.models import Event
from venues.models import Venue
from clients.models import Client
from django.core import serializers
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required


# AJAX RESPONSE MIXIN WHICH I DON'T KNOW WHAT IT DOES
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


# MAIN INDEX VIEW
class IndexView(LoginRequiredMixin, ListView):
	login_url = '/accounts/login/'
	model = Question
	template_name = 'faq/faq.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.user.profile.client == 'Livecrowd':
			venue_list = Venue.objects.all()
			client_list = Client.objects.all()
		elif not self.request.user.profile.client:
			venue_list = Venue.objects.all()
			client_list = Client.objects.all()
		else:
			venue_list = Venue.objects.filter(client=self.request.user.profile.client)
			client_name = self.request.user.profile.client
			client_list = Client.objects.filter(name=client_name)
		context['venue_list'] = venue_list
		context['client_list'] = client_list
		return context


# # MAIN EVENT VIEW
# class EventView(LoginRequiredMixin, ListView):
# 	login_url = '/accounts/login/'
# 	model = Question
# 	template_name = 'faq/faq.html'
#
# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		events_list = Event.objects.all()
# 		context['events_list'] = events_list
# 		return context
#
# 	def get_queryset(self):
# 		event = Event.objects.get(event=self.kwargs['event'])
# 		queryset = Question.objects.filter(event=event)
# 		return queryset
#
# 	def get(self, request, *args, **kwargs):
# 		queryset = self.get_queryset()
# 		data = serializers.serialize("json", queryset, use_natural_foreign_keys=True)
# 		return JsonResponse(data, status=200, safe=False)


# QUESTION COUNT PLUS +1
@login_required
def CountPlus(request, pk):
	if request.method == 'POST':
		question = Question.objects.get(pk=request.POST['pk'])
		# print(question)
		question.count += 1
		# print(question.count)
		question.save()
		return HttpResponse("OK")
	else:
		pass


# QUESTION CREATE VIEW
@login_required
def QuestionCreate(request):
	if request.method == 'POST':
		question = request.POST['question']
		answer = request.POST['answer']
		category = Category.objects.get(category=request.POST['category'])
		event = Event.objects.get(event=request.POST['event'])
		user_created = request.user
		Question.objects.create(question=question, answer=answer, category=category, event=event,
								user_created=user_created)
		# question.save()
		return HttpResponse("OK")
	else:
		return HttpResponse("FORM INVALID")


# QUESTION UPDATE VIEW
# ! request, pk <-- PK is not needed. next version remove from url.
@login_required
def QuestionUpdate(request, pk):
	if request.method == 'POST':
		query = Question.objects.get(pk=pk)
		query.question = request.POST['question']
		query.answer = request.POST['answer']
		query.user_created = request.user
		query.save()
		return HttpResponse("OK")
	else:
		return HttpResponse("FORM INVALID")


# GET ALL CATEGORIES FOR MODEL CREATION AND UPDATE
@login_required
def CategoriesGet(request):
	queryset_categories = Category.objects.all()
	data = serializers.serialize("json", queryset_categories, use_natural_foreign_keys=True)
	return JsonResponse(data, status=200, safe=False)


# GET ALL EVENTS FOR SIDEBAR, MODEL CREATION AND UPDATE
# TODO: filter only the valid ones. The expired events (after 1 week should not be presented)
@login_required
def EventsGet(request):
	if request.user.profile.client == None:
		queryset_events = Event.objects.all()
	elif request.user.profile.client == 'Livecrowd':
		queryset_events = Event.objects.all()
	else:
		client = request.user.profile.client
		queryset_events = Event.objects.filter(venue__client=client)

	data = serializers.serialize("json", queryset_events, use_natural_foreign_keys=True)
	return JsonResponse(data, status=200, safe=False)


@login_required
def EventInfoGet(request):
	key_list = []
	for key in request.GET.getlist('pk'):
		key_list.append(key)
	queryset = Event.objects.filter(pk__in=key_list)
	data = serializers.serialize("json", queryset, use_natural_foreign_keys=True)
	return JsonResponse(data, status=200, safe=False)


# NEW:
@login_required
def QuestionQueryset(request):
	key_list = []
	for key in request.GET.getlist('pk'):
		key_list.append(key)

	query = Question.objects.filter(event__pk__in=key_list, is_archived=False)
	data = serializers.serialize("json", query, use_natural_foreign_keys=True)
	return JsonResponse(data, status=200, safe=False)


# q = Question.objects.filter(Q(event__pk=1) | Q(event__pk=5))

@login_required
def AllQuestions(request):
	"""
	This function returns all questions in a JSON Query if the user is a Livecrowd user.
	If the user is not a livecrowd user then it returns all questions of their group (Client model)
	When you click on ALLES or ALL in the client navigation balk it GETs at /query/all

	:param request:
	:return:
	"""
	if not request.user.profile.client or request.user.profile.client == "Livecrowd":
		query = Question.objects.filter(is_archived=False)
	else:
		query = Question.objects.filter(client=request.user.profile.client, is_archived=False)
	data = serializers.serialize("json", query, use_natural_foreign_keys=True)
	return JsonResponse(data, status=200, safe=False)


@login_required
def DeleteQuestion(request, pk):
	question = Question.objects.get(pk=pk).delete()
	return HttpResponse("OK")


@login_required
def ArchiveQuestion(request, pk):
	question = Question.objects.get(pk=pk)
	question.is_archived = True
	question.save()
	return HttpResponse("OK")
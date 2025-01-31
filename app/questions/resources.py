from import_export import resources
from .models import Question
from import_export.widgets import ForeignKeyWidget, DateTimeWidget

class QuestionResource(resources.ModelResource):
	category = fields.Field(
			column_name='category',
			attribute='category',
			widget=ForeignKeyWidget(Category, 'category')
		)
	created = fields.Field(
		column_name='created',
		attribute='created',
		widget=DateTimeWidget(format="%d/%m/%Y %H:%M"))

	class Meta:
		model = Question
		fields = ['id', 'question', 'category', 'answer',]

		# exclude = ('created', 'modified', 'verified', 'count', 'user_created')
	
	# def _post_import(model, **kwargs):
	# 	query = self.fields['category']
	# 	category = Question.objects.get_or_create(category=query)
	# 	return category

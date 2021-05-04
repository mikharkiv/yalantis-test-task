import datetime
import json

from django import views
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views import View
from django.views.generic.edit import BaseCreateView, ModelFormMixin, BaseUpdateView

from course_catalogue.settings import PURE_REST
from course_catalogue.views.filters import SearchFilter, FieldsFilter


class DateDjangoJSONEncoder(DjangoJSONEncoder):
	"""
	Default Django JSON Encoder with custom date format support
	"""
	def default(self, o):
		if isinstance(o, datetime.date):
			return format(o, PURE_REST['DATE_FORMAT'])
		else:
			return super().default(o)


class JsonResponseMixin:
	"""
	Mixin for returning JSON response (with pagination, if possible)
	"""
	def render_to_response(self, context, **response_kwargs):
		return JsonResponse(self.get_paginated_data(context), **response_kwargs, safe=False, encoder=DateDjangoJSONEncoder)

	def get_data(self, context):
		return context

	def get_paginated_data(self, context):
		# A simple pagination
		if context.get('paginator', None):
			paginator = context['paginator']
			return {'count': paginator.count,
					'total_pages': paginator.num_pages,
					'results': self.get_data(context)}
		else:
			return self.get_data(context)


class JsonListView(JsonResponseMixin, views.generic.list.BaseListView):
	"""
	Default Django List View with JSON response
	"""
	paginate_by = PURE_REST['PAGE_SIZE']  # Default pages count

	def get_data(self, context):
		return list(context['object_list'].values().iterator())


class JsonDetailView(JsonResponseMixin, views.generic.detail.BaseDetailView):
	"""
	Default Django Detail View with JSON response
	"""
	def get_data(self, context):
		return model_to_dict(context['object'])


class JsonFormMixin(ModelFormMixin):
	"""
	That mixin allows to use default Django Form Processing API
	with JSON requests
	"""
	def get_form(self, form_class=None):
		kwargs = self.get_form_kwargs()
		if form_class is None:
			form_class = self.get_form_class()
		# Primitive and naive deserialization (w/o writing own Serializer)
		try:
			kwargs['data'] = json.loads(self.request.body)
			return form_class(**kwargs)
		except json.JSONDecodeError:
			# If an error occurred, assume that reason is the bad JSON
			return form_class()

	def form_valid(self, form):
		self.object = form.save()
		# Primitive and naive serialization (w/o writing own Serializer)
		return JsonResponse(model_to_dict(self.object), safe=False, encoder=DateDjangoJSONEncoder)


class JsonFormProcessor(JsonFormMixin, View):
	"""
	Default Django form processor modified for using with JSON and has
	restricted GET method
	"""
	def get(self, request, *args, **kwargs):
		# Restrict for using GET method inherited from superclass
		return JsonResponse({'detail': 'Method not allowed'}, status=405, encoder=DateDjangoJSONEncoder)

	def post(self, request, *args, **kwargs):
		form = self.get_form()
		if form.is_valid():
			return self.form_valid(form)
		else:
			# If we have some problems, return form errors
			return JsonResponse(form.errors, status=400, encoder=DateDjangoJSONEncoder)


class JsonCreateView(BaseCreateView, JsonFormProcessor):
	"""
	Default Django Create View that accepts JSON-encoded data with
	restricted GET method
	"""


class JsonUpdateView(BaseUpdateView, JsonFormProcessor):
	"""
	Default Django Update View that accepts JSON-encoded data with
	restricted GET method
	"""


class JsonDeleteView(JsonFormProcessor):
	"""
	A Delete View with restricted GET method, returns
	JSON-encoded response
	"""
	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		self.object.delete()
		return JsonResponse({'detail': 'Object deleted'}, encoder=DateDjangoJSONEncoder)


class JsonModelView(JsonDetailView, JsonUpdateView, JsonDeleteView):
	"""
	Provides multiple views for model:
		GET - Detail JSON view.

		POST - Update JSON view.

		DELETE - Delete JSON view.
	"""


class JsonListCreateView(FieldsFilter, SearchFilter, JsonListView, JsonCreateView):
	"""
	Uses FieldsFilter and SearchFilter.
	Provides multiple list views for model:
		GET - List JSON view.

		POST - Create JSON view.
	"""
	object = None

from django.core.exceptions import ValidationError
from django.views.generic.list import MultipleObjectMixin


class SearchFilter(MultipleObjectMixin):
	"""
	A simple and naive search filter. Checking if query appears in search_fields
	using `icontains` lookup
	"""
	search_fields = []

	def get_queryset(self):
		query = self.request.GET.get('search', None)

		if self.search_fields and query:
			filter_dict = {field + '__icontains': query for field in self.search_fields}
			return super().get_queryset().filter(**filter_dict)
		else:
			return super().get_queryset()


class FieldsFilter(MultipleObjectMixin):
	"""
	A simple and naive fields filter working with basic lookups:
	`gte, lte, exact, gt, lt`
	"""
	filter_fields = []

	def get_queryset(self):
		default_lookups = ['gte', 'lte', 'exact', 'gt', 'lt']
		filter_names = [field + '__' + lookup for field in self.filter_fields for lookup in default_lookups]
		# Appending for filtering EXACT without __exact lookup in request
		filter_names.extend(self.filter_fields)
		filters = {name: self.request.GET[name] for name in filter_names if self.request.GET.get(name, None)}

		try:
			return super().get_queryset().filter(**filters)
		except ValidationError:
			return super().get_queryset()

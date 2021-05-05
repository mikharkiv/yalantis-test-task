from rest_framework import viewsets
from .serializers import CourseSerializer
from .models import Course
from views.json import JsonModelView, JsonListCreateView


class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	search_fields = ['name']
	ordering_fields = '__all__'
	filterset_fields = {'start_date': ['gte', 'lte', 'exact', 'gt', 'lt'],
						'end_date': ['gte', 'lte', 'exact', 'gt', 'lt']}


class CourseModelView(JsonModelView):
	model = Course
	fields = '__all__'


class CourseListCreateView(JsonListCreateView):
	model = Course
	fields = '__all__'
	search_fields = ['name']
	filter_fields = ['start_date', 'end_date']

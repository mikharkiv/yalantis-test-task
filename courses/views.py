from rest_framework import viewsets
from .serializers import CourseSerializer
from .models import Course
from .json import *


class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	search_fields = '__all__'
	ordering_fields = '__all__'
	filterset_fields = '__all__'


class CourseModelView(JsonModelView):
	model = Course
	fields = '__all__'


class CourseListCreateView(JsonListCreateView):
	model = Course
	fields = '__all__'

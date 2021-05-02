from rest_framework import viewsets
from .serializers import CourseSerializer
from .models import Course


class CourseViewSet(viewsets.ModelViewSet):
	queryset = Course.objects.all()
	serializer_class = CourseSerializer
	search_fields = '__all__'
	ordering_fields = '__all__'
	filterset_fields = '__all__'

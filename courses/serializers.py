from rest_framework import serializers
from .models import Course


class CourseSerializer(serializers.ModelSerializer):
	"""
	Default serializer for Course model
	"""
	class Meta:
		model = Course
		fields = '__all__'

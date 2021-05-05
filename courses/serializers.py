from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Course


class CourseSerializer(serializers.ModelSerializer):
	"""
	Default serializer for Course model
	"""
	class Meta:
		model = Course
		fields = '__all__'

	def validate(self, attrs):
		if attrs['start_date'] > attrs['end_date']:
			raise ValidationError('Start date should precede end date')
		if attrs['lectures_num'] < 0:
			raise ValidationError('Number of lectures should be a natural number')
		return attrs

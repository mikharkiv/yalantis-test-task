from django.db import models


class Course(models.Model):
	"""
	The model of the course.
	"""

	name = models.CharField(max_length=50, verbose_name='name')
	start_date = models.DateField(verbose_name='date of start')
	end_date = models.DateField(verbose_name='date of end')
	lectures_num = models.PositiveIntegerField(verbose_name='number of lectures')

	def __str__(self):
		return self.name

from django.urls import path
from .views import CourseListCreateView, CourseModelView


urlpatterns = [
	path('courses/', CourseListCreateView.as_view(), name='pure-course-list'),
	path('courses/<int:pk>/', CourseModelView.as_view(), name='pure-course-detail'),
]

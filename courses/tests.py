import json
from urllib.parse import urlencode

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from courses.models import Course


class DRFCourseAPITest(APITestCase):
	entities = []

	def setUp(self) -> None:
		self.entities.append(Course.objects.create(
			name='Test1', start_date='2001-01-01', end_date='2001-02-01',
			lectures_num=8))
		self.entities.append(Course.objects.create(
			name='Test2', start_date='2002-01-01', end_date='2002-02-01',
			lectures_num=5))

	def test_list(self):
		url = reverse('course-list')
		response = self.client.get(url, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['count'], 2)

	def test_detail(self):
		url = reverse('course-detail', kwargs={'pk': self.entities[-1].id})
		response = self.client.get(url, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIsNotNone(response.data['name'])
		self.assertIsNotNone(response.data['start_date'])
		self.assertIsNotNone(response.data['end_date'])
		self.assertIsNotNone(response.data['lectures_num'])

	def test_create(self):
		url = reverse('course-list')
		entity = {'name': 'Test3', 'start_date': '01.01.2003',
					'end_date': '01.02.2003', 'lectures_num': 8}
		response = self.client.post(url, entity, format='json')
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertIsNotNone(response.data['name'])
		self.assertIsNotNone(response.data['start_date'])
		self.assertIsNotNone(response.data['end_date'])
		self.assertIsNotNone(response.data['lectures_num'])
		self.entities.append(Course(**response.data))

	def test_create_validation(self):
		url = reverse('course-list')
		entity = {'name': 'TestBad', 'start_date': '01.02.2003',
					'end_date': '01.01.2002', 'lectures_num': 8}
		response = self.client.post(url, entity, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		entity = {'name': 'TestBad', 'start_date': '01.02.2003',
					'end_date': '01.01.2003', 'lectures_num': -1}
		response = self.client.post(url, entity, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		entity = {'name': '', 'start_date': '01.02.2003',
					'end_date': '01.01.2003', 'lectures_num': -1}
		response = self.client.post(url, entity, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_modify(self):
		url = reverse('course-detail', kwargs={'pk': self.entities[-1].id})
		entity = {'name': 'Test333', 'start_date': '02.01.2003',
					'end_date': '02.02.2003', 'lectures_num': 7}
		response = self.client.put(url, entity, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIsNotNone(response.data['name'])
		self.assertIsNotNone(response.data['start_date'])
		self.assertIsNotNone(response.data['end_date'])
		self.assertIsNotNone(response.data['lectures_num'])

	def test_filter(self):
		url = reverse('course-list')
		# Testing EXACT
		filters = {'start_date': '2001-01-01', 'end_date': '2001-02-01'}
		response = self.client.get(url + '?' + urlencode(filters), format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['count'], 1)
		# Testing GreaterThan and LowerThanOrEqual
		filters = {'start_date__gt': '2000-01-01', 'end_date__lte': '2001-02-01'}
		response = self.client.get(url + '?' + urlencode(filters), format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['count'], 1)

	def test_search(self):
		url = reverse('course-list')
		search = {'search': 'tes'}
		response = self.client.get(url + '?' + urlencode(search), format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['count'], 2)

	def test_delete(self):
		url = reverse('course-detail', kwargs={'pk': self.entities[-1].id})
		response = self.client.delete(url, format='json')
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PureCourseAPITest(APITestCase):
	entities = []

	def setUp(self) -> None:
		self.entities.append(Course.objects.create(
			name='Test1', start_date='2001-01-01', end_date='2001-02-01',
			lectures_num=8))
		self.entities.append(Course.objects.create(
			name='Test2', start_date='2002-01-01', end_date='2002-02-01',
			lectures_num=5))

	def test_list(self):
		url = reverse('pure-course-list')
		response = self.client.get(url, format='json')
		body = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(body['count'], 2)

	def test_detail(self):
		url = reverse('pure-course-detail', kwargs={'pk': self.entities[-1].id})
		response = self.client.get(url, format='json')
		body = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIsNotNone(body['name'])
		self.assertIsNotNone(body['start_date'])
		self.assertIsNotNone(body['end_date'])
		self.assertIsNotNone(body['lectures_num'])

	def test_create(self):
		url = reverse('pure-course-list')
		entity = {'name': 'Test3', 'start_date': '01.01.2003',
					'end_date': '01.02.2003', 'lectures_num': 8}
		response = self.client.post(url, entity, format='json')
		body = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIsNotNone(body['name'])
		self.assertIsNotNone(body['start_date'])
		self.assertIsNotNone(body['end_date'])
		self.assertIsNotNone(body['lectures_num'])
		self.entities.append(Course(**body))

	def test_create_validation(self):
		url = reverse('pure-course-list')
		entity = {'name': 'TestBad', 'start_date': '01.02.2003',
					'end_date': '01.01.2002', 'lectures_num': 8}
		response = self.client.post(url, entity, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		entity = {'name': 'TestBad', 'start_date': '01.02.2003',
					'end_date': '01.01.2003', 'lectures_num': -1}
		response = self.client.post(url, entity, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

		entity = {'name': '', 'start_date': '01.02.2003',
					'end_date': '01.01.2003', 'lectures_num': -1}
		response = self.client.post(url, entity, format='json')
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_modify(self):
		url = reverse('pure-course-detail', kwargs={'pk': self.entities[-1].id})
		entity = {'name': 'Test333', 'start_date': '02.01.2003',
					'end_date': '02.02.2003', 'lectures_num': 7}
		response = self.client.put(url, entity, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		body = json.loads(response.content)
		self.assertIsNotNone(body['name'])
		self.assertIsNotNone(body['start_date'])
		self.assertIsNotNone(body['end_date'])
		self.assertIsNotNone(body['lectures_num'])

	def test_filter(self):
		url = reverse('pure-course-list')
		# Testing EXACT
		filters = {'start_date': '2001-01-01', 'end_date': '2001-02-01'}
		response = self.client.get(url + '?' + urlencode(filters), format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		body = json.loads(response.content)
		self.assertEqual(body['count'], 1)
		# Testing GreaterThan and LowerThanOrEqual
		filters = {'start_date__gt': '2000-01-01', 'end_date__lte': '2001-02-01'}
		response = self.client.get(url + '?' + urlencode(filters), format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		body = json.loads(response.content)
		self.assertEqual(body['count'], 1)

	def test_search(self):
		url = reverse('pure-course-list')
		search = {'search': 'tes'}
		response = self.client.get(url + '?' + urlencode(search), format='json')
		body = json.loads(response.content)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(body['count'], 2)

	def test_delete(self):
		url = reverse('pure-course-detail', kwargs={'pk': self.entities[-1].id})
		response = self.client.delete(url, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

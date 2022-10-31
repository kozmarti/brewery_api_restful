import json
from rest_framework import status
from django.test import TestCase, Client
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase, APISimpleTestCase, APITransactionTestCase
from beermanagment.views import ReferenceViewSet, statistics
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User

class TestCaseForReference(APITestCase):
	fixtures = ["fixtures.json"]


	def test_post_reference_request_factory(self):
		user_staff = User.objects.get(username='marta_staff')
		user_customer = User.objects.get(username='marta_customer')

		request_factory = APIRequestFactory()
		request = request_factory.post("/api/references/", {'reference': 'new', 'name': 'new beer'})
		reference_view = ReferenceViewSet.as_view({'post': 'create'})
		response = reference_view(request)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
		force_authenticate(request, user=user_staff)
		response = reference_view(request)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		force_authenticate(request, user=user_customer)
		response = reference_view(request)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_get_statistics_request_factory(self):
		request_factory = APIRequestFactory()
		request = request_factory.get("/api/statistics/")
		reference_view = statistics
		response = reference_view(request)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
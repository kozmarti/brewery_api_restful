from rest_framework import status
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from beermanagment.views import ReferenceViewSet, BarViewSet, OrderList, statistics, StockViewSet
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
from parameterized import parameterized


class TestCaseForObjects(APITestCase):
    fixtures = ["fixtures.json"]
    user_staff = User.objects.get(username='marta_staff')
    user_customer = User.objects.get(username='marta_customer')
    request_factory = APIRequestFactory()
    request_factory_url_reference = "/api/references/"
    request_factory_url_bar = "/api/bars/"
    request_factory_url_order = "/api/orers/"
    request_factory_url_stock = "/api/ors/"

    @parameterized.expand([
        ("Staff user GET LIST", user_staff, request_factory.get(request_factory_url_reference), {'get': 'list'}, status.HTTP_200_OK),
        ("Customer user GET LIST", user_customer, request_factory.get(request_factory_url_reference), {'get': 'list'}, status.HTTP_200_OK),
        ("Anonyme GET LIST", None, request_factory.get(request_factory_url_reference), {'get': 'list'}, status.HTTP_200_OK),
        ("Staff user GET RETRIEVE", user_staff, request_factory.get(request_factory_url_reference), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Customer user GET RETRIEVE", user_customer, request_factory.get(request_factory_url_reference), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Anonyme GET RETRIEVE", None, request_factory.get(request_factory_url_reference), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Staff user POST", user_staff, request_factory.post(request_factory_url_reference, {'reference': 'new', 'name': 'new beer'}), {'post': 'create'}, status.HTTP_201_CREATED),
        ("Staff user POST WRONG", user_staff, request_factory.post(request_factory_url_reference, {'bad attribute': 'wrong data'}), {'post': 'create'}, status.HTTP_400_BAD_REQUEST),
        ("Customer user POST", user_customer, request_factory.post(request_factory_url_reference, {'reference': 'new', 'name': 'new beer'}),  {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme POST", None, request_factory.post(request_factory_url_reference, {'reference': 'new', 'name': 'new beer'}),  {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Staff user PUT", user_staff, request_factory.put(request_factory_url_reference, {'reference': 'modified', 'name': 'modified'}), {'put': 'update'}, status.HTTP_200_OK),
        ("Staff user PUT WRONG", user_staff, request_factory.put(request_factory_url_reference,  {'bad attribute': 'wrong data'}), {'put': 'update'}, status.HTTP_400_BAD_REQUEST),
        ("Customer user PUT", user_customer, request_factory.put(request_factory_url_reference, {'reference': 'modified', 'name': 'modified'}), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme PUT", None, request_factory.put(request_factory_url_reference, {'reference': 'modified', 'name': 'modified'}), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Staff user DELETE", user_staff, request_factory.delete(request_factory_url_reference), {'delete': 'destroy'}, status.HTTP_204_NO_CONTENT),
        ("Customer user DELETE", user_customer, request_factory.delete(request_factory_url_reference), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme DELETE", None, request_factory.delete(request_factory_url_reference), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
    ])
    def test_reference_views_responses(self, _, currentuser, request, view, expected):
        reference_view = ReferenceViewSet.as_view(view)
        if currentuser:
            force_authenticate(request, user=currentuser)
        response = reference_view(request, pk=1)
        self.assertEqual(response.status_code, expected)

    @parameterized.expand([
        ("Staff user GET LIST", user_staff, request_factory.get(request_factory_url_bar), {'get': 'list'}, status.HTTP_200_OK),
        ("Customer user GET LIST", user_customer, request_factory.get(request_factory_url_bar), {'get': 'list'}, status.HTTP_200_OK),
        ("Anonyme GET LIST", None, request_factory.get(request_factory_url_bar), {'get': 'list'}, status.HTTP_200_OK),
        ("Staff user GET RETRIEVE", user_staff, request_factory.get(request_factory_url_bar), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Customer user GET RETRIEVE", user_customer, request_factory.get(request_factory_url_bar), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Anonyme GET RETRIEVE", None, request_factory.get(request_factory_url_bar), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Staff user POST", user_staff, request_factory.post(request_factory_url_bar, {'name': 'new bar'}), {'post': 'create'}, status.HTTP_201_CREATED),
        ("Staff user POST WRONG", user_staff, request_factory.post(request_factory_url_bar, {'bad attribute': 'wrong data'}), {'post': 'create'}, status.HTTP_400_BAD_REQUEST),
        ("Customer user POST", user_customer, request_factory.post(request_factory_url_bar, {'name': 'new bar'}),  {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme POST", None, request_factory.post(request_factory_url_bar, {'name': 'new bar'}),  {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Staff user PUT", user_staff, request_factory.put(request_factory_url_bar, {'name': 'modified'}), {'put': 'update'}, status.HTTP_200_OK),
        ("Staff user PUT WRONG", user_staff, request_factory.put(request_factory_url_bar,  {'bad attribute': 'wrong data'}), {'put': 'update'}, status.HTTP_400_BAD_REQUEST),
        ("Customer user PUT", user_customer, request_factory.put(request_factory_url_bar, {'name': 'modified'}), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme PUT", None, request_factory.put(request_factory_url_bar, {'name': 'modified'}), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Staff user DELETE", user_staff, request_factory.delete(request_factory_url_bar), {'delete': 'destroy'}, status.HTTP_204_NO_CONTENT),
        ("Customer user DELETE", user_customer, request_factory.delete(request_factory_url_bar), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme DELETE", None, request_factory.delete(request_factory_url_bar), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
    ])
    def test_bar_views_responses(self, _, currentuser, request, view, expected):
        reference_view = BarViewSet.as_view(view)
        if currentuser:
            force_authenticate(request, user=currentuser)
        response = reference_view(request, pk=1)
        self.assertEqual(response.status_code, expected)

    @parameterized.expand([
        ("Staff user GET LIST", user_staff, request_factory.get(request_factory_url_order), status.HTTP_200_OK),
        ("Customer user GET LIST", user_customer, request_factory.get(request_factory_url_order), status.HTTP_200_OK),  # check content that no queryset can be viewed
        ("Anonyme GET LIST", None, request_factory.get(request_factory_url_order), status.HTTP_200_OK),  # check content that no queryset can be viewed
        ("Staff user GET RETRIEVE", user_staff, request_factory.get(request_factory_url_order), status.HTTP_200_OK),
        ("Customer user GET RETRIEVE", user_customer, request_factory.get(request_factory_url_order), status.HTTP_200_OK),  # check content that no object can be viewed
        ("Anonyme GET RETRIEVE", None, request_factory.get(request_factory_url_order), status.HTTP_200_OK),  # check content that no object can be viewed
        ("Staff user POST", user_staff, request_factory.post(request_factory_url_order, {'bar': 1, 'items': []}), status.HTTP_403_FORBIDDEN),
        ("Customer user POST", user_customer, request_factory.post(request_factory_url_order, {'bar': 1, 'items': []}),  status.HTTP_201_CREATED),
        ("Customer user POST WRONG", user_customer, request_factory.post(request_factory_url_order, {'wrong attribute': 1, 'items': []}),  status.HTTP_400_BAD_REQUEST),
        ("Anonyme POST", None, request_factory.post(request_factory_url_order, {'bar': 1, 'items': []}),  status.HTTP_201_CREATED),
        ("Staff user PUT", user_staff, request_factory.put(request_factory_url_order, {'bar': 1, 'items': []}), status.HTTP_403_FORBIDDEN),
        ("Customer user PUT", user_customer, request_factory.put(request_factory_url_order, {'bar': 1, 'items': []}), status.HTTP_403_FORBIDDEN),
        ("Anonyme PUT", None, request_factory.put(request_factory_url_order, {'bar': 1, 'items': []}), status.HTTP_403_FORBIDDEN),
        ("Staff user DELETE", user_staff, request_factory.delete(request_factory_url_order), status.HTTP_403_FORBIDDEN),
        ("Customer user DELETE", user_customer, request_factory.delete(request_factory_url_order), status.HTTP_403_FORBIDDEN),
        ("Anonyme DELETE", None, request_factory.delete(request_factory_url_order), status.HTTP_403_FORBIDDEN),
    ])
    def test_order_views_responses(self, _, currentuser, request, expected):
        reference_view = OrderList.as_view()
        if currentuser:
            force_authenticate(request, user=currentuser)
        response = reference_view(request)
        self.assertEqual(response.status_code, expected)

    @parameterized.expand([
        ("Staff user GET", user_staff, request_factory.get("/api/statistics/"), status.HTTP_200_OK),
        ("Customer user GET", user_customer, request_factory.get("/api/statistics/"), status.HTTP_403_FORBIDDEN),
        ("Anonyme GET", None, request_factory.get("/api/statistics/"), status.HTTP_403_FORBIDDEN),
    ])
    def test_statistic_view_responses(self, _, currentuser, request, expected):
        reference_view = statistics
        if currentuser:
            force_authenticate(request, user=currentuser)
        response = reference_view(request)
        self.assertEqual(response.status_code, expected)

    @parameterized.expand([
        ("Staff user GET LIST", user_staff, request_factory.get(request_factory_url_stock), {'get': 'list'}, status.HTTP_200_OK),
        ("Customer user GET LIST", user_customer, request_factory.get(request_factory_url_stock), {'get': 'list'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme GET LIST", None, request_factory.get(request_factory_url_stock), {'get': 'list'}, status.HTTP_403_FORBIDDEN),
        ("Staff user GET RETRIEVE", user_staff, request_factory.get(request_factory_url_stock), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Customer user GET RETRIEVE", user_customer, request_factory.get(request_factory_url_stock), {'get': 'retrieve'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme GET RETRIEVE", None, request_factory.get(request_factory_url_stock), {'get': 'retrieve'}, status.HTTP_403_FORBIDDEN),
        ("Staff user POST", user_staff, request_factory.post(request_factory_url_stock), {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Customer user POST", user_customer, request_factory.post(request_factory_url_stock),  {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme POST", None, request_factory.post(request_factory_url_stock),  {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Staff user PUT", user_staff, request_factory.put(request_factory_url_stock, {'reference': 'modified', 'name': 'modified'}), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Customer user PUT", user_customer, request_factory.put(request_factory_url_stock), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme PUT", None, request_factory.put(request_factory_url_stock), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Staff user DELETE", user_staff, request_factory.delete(request_factory_url_stock), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
        ("Customer user DELETE", user_customer, request_factory.delete(request_factory_url_stock), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme DELETE", None, request_factory.delete(request_factory_url_stock), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
    ])
    def test_stock_views_responses(self, _, currentuser, request, view, expected):
        reference_view = StockViewSet.as_view(view)
        if currentuser:
            force_authenticate(request, user=currentuser)
        response = reference_view(request, pk=1)
        self.assertEqual(response.status_code, expected)

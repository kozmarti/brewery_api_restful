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

    @parameterized.expand([
        ("Staff user GET LIST", user_staff, request_factory.get("/api/references/"), {'get': 'list'}, status.HTTP_200_OK),
        ("Customer user GET LIST", user_customer, request_factory.get("/api/references/"), {'get': 'list'}, status.HTTP_200_OK),
        ("Anonyme GET LIST", None, request_factory.get("/api/references/"), {'get': 'list'}, status.HTTP_200_OK),
        ("Staff user GET RETRIEVE", user_staff, request_factory.get("/api/references/"), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Customer user GET RETRIEVE", user_customer, request_factory.get("/api/references/"), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Anonyme GET RETRIEVE", None, request_factory.get("/api/references/"), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Staff user POST", user_staff, request_factory.post("/api/references/", {'reference': 'new', 'name': 'new beer'}), {'post': 'create'}, status.HTTP_201_CREATED),
        ("Staff user POST WRONG", user_staff, request_factory.post("/api/references/", {'bad attribute': 'wrong data'}), {'post': 'create'}, status.HTTP_400_BAD_REQUEST),
        ("Customer user POST", user_customer, request_factory.post("/api/references/", {'reference': 'new', 'name': 'new beer'}),  {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme POST", None, request_factory.post("/api/references/", {'reference': 'new', 'name': 'new beer'}),  {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Staff user PUT", user_staff, request_factory.put("/api/references/1", {'reference': 'modified', 'name': 'modified'}), {'put': 'update'}, status.HTTP_200_OK),
        ("Staff user PUT WRONG", user_staff, request_factory.put("/api/references/1",  {'bad attribute': 'wrong data'}), {'put': 'update'}, status.HTTP_400_BAD_REQUEST),
        ("Customer user PUT", user_customer, request_factory.put("/api/references/1", {'reference': 'modified', 'name': 'modified'}), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme PUT", None, request_factory.put("/api/references/1", {'reference': 'modified', 'name': 'modified'}), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Staff user DELETE", user_staff, request_factory.delete("/api/references/1"), {'delete': 'destroy'}, status.HTTP_204_NO_CONTENT),
        ("Customer user DELETE", user_customer, request_factory.delete("/api/references/1"), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme DELETE", None, request_factory.delete("/api/references/1"), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
    ])
    def test_reference_views_responses(self, _, currentuser, request, view, expected):
        reference_view = ReferenceViewSet.as_view(view)
        if currentuser:
            force_authenticate(request, user=currentuser)
        response = reference_view(request, pk=1)
        self.assertEqual(response.status_code, expected)

    @parameterized.expand([
        ("Staff user GET LIST", user_staff, request_factory.get("/api/bars/"), {'get': 'list'}, status.HTTP_200_OK),
        ("Customer user GET LIST", user_customer, request_factory.get("/api/bars/"), {'get': 'list'}, status.HTTP_200_OK),
        ("Anonyme GET LIST", None, request_factory.get("/api/bars/"), {'get': 'list'}, status.HTTP_200_OK),
        ("Staff user GET RETRIEVE", user_staff, request_factory.get("/api/bars/"), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Customer user GET RETRIEVE", user_customer, request_factory.get("/api/bars/"), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Anonyme GET RETRIEVE", None, request_factory.get("/api/bars/"), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Staff user POST", user_staff, request_factory.post("/api/bars/", {'name': 'new bar'}), {'post': 'create'}, status.HTTP_201_CREATED),
        ("Staff user POST WRONG", user_staff, request_factory.post("/api/bars/", {'bad attribute': 'wrong data'}), {'post': 'create'}, status.HTTP_400_BAD_REQUEST),
        ("Customer user POST", user_customer, request_factory.post("/api/bars/", {'name': 'new bar'}),  {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme POST", None, request_factory.post("/api/bars/", {'name': 'new bar'}),  {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Staff user PUT", user_staff, request_factory.put("/api/bars/1", {'name': 'modified'}), {'put': 'update'}, status.HTTP_200_OK),
        ("Staff user PUT WRONG", user_staff, request_factory.put("/api/bars/1",  {'bad attribute': 'wrong data'}), {'put': 'update'}, status.HTTP_400_BAD_REQUEST),
        ("Customer user PUT", user_customer, request_factory.put("/api/bars/1", {'name': 'modified'}), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme PUT", None, request_factory.put("/api/bars/1", {'name': 'modified'}), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Staff user DELETE", user_staff, request_factory.delete("/api/bars/1"), {'delete': 'destroy'}, status.HTTP_204_NO_CONTENT),
        ("Customer user DELETE", user_customer, request_factory.delete("/api/bars/1"), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme DELETE", None, request_factory.delete("/api/bars/1"), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
    ])
    def test_bar_views_responses(self, _, currentuser, request, view, expected):
        reference_view = BarViewSet.as_view(view)
        if currentuser:
            force_authenticate(request, user=currentuser)
        response = reference_view(request, pk=1)
        self.assertEqual(response.status_code, expected)

    @parameterized.expand([
        ("Staff user GET LIST", user_staff, request_factory.get("/api/orders/"), status.HTTP_200_OK),
        ("Customer user GET LIST", user_customer, request_factory.get("/api/orders/"), status.HTTP_200_OK),  # check content that no queryset can be viewed
        ("Anonyme GET LIST", None, request_factory.get("/api/orders/"), status.HTTP_200_OK),  # check content that no queryset can be viewed
        ("Staff user GET RETRIEVE", user_staff, request_factory.get("/api/orders/"), status.HTTP_200_OK),
        ("Customer user GET RETRIEVE", user_customer, request_factory.get("/api/orders/"), status.HTTP_200_OK),  # check content that no object can be viewed
        ("Anonyme GET RETRIEVE", None, request_factory.get("/api/orders/"), status.HTTP_200_OK),  # check content that no object can be viewed
        ("Staff user POST", user_staff, request_factory.post("/api/orders/", {'bar': 1, 'items': []}), status.HTTP_403_FORBIDDEN),
        ("Customer user POST", user_customer, request_factory.post("/api/orders/", {'bar': 1, 'items': []}),  status.HTTP_201_CREATED),
        ("Customer user POST WRONG", user_customer, request_factory.post("/api/orders/", {'wrong attribute': 1, 'items': []}),  status.HTTP_400_BAD_REQUEST),
        ("Anonyme POST", None, request_factory.post("/api/orders/", {'bar': 1, 'items': []}),  status.HTTP_201_CREATED),
        ("Staff user PUT", user_staff, request_factory.put("/api/orders/1", {'bar': 1, 'items': []}), status.HTTP_403_FORBIDDEN),
        ("Customer user PUT", user_customer, request_factory.put("/api/orders/1", {'bar': 1, 'items': []}), status.HTTP_403_FORBIDDEN),
        ("Anonyme PUT", None, request_factory.put("/api/orders/1", {'bar': 1, 'items': []}), status.HTTP_403_FORBIDDEN),
        ("Staff user DELETE", user_staff, request_factory.delete("/api/orders/1"), status.HTTP_403_FORBIDDEN),
        ("Customer user DELETE", user_customer, request_factory.delete("/api/orders/1"), status.HTTP_403_FORBIDDEN),
        ("Anonyme DELETE", None, request_factory.delete("/api/orders/1"), status.HTTP_403_FORBIDDEN),
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
        ("Staff user GET LIST", user_staff, request_factory.get("/api/stocks/"), {'get': 'list'}, status.HTTP_200_OK),
        ("Customer user GET LIST", user_customer, request_factory.get("/api/stocks/"), {'get': 'list'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme GET LIST", None, request_factory.get("/api/stocks/"), {'get': 'list'}, status.HTTP_403_FORBIDDEN),
        ("Staff user GET RETRIEVE", user_staff, request_factory.get("/api/stocks/"), {'get': 'retrieve'}, status.HTTP_200_OK),
        ("Customer user GET RETRIEVE", user_customer, request_factory.get("/api/stocks/"), {'get': 'retrieve'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme GET RETRIEVE", None, request_factory.get("/api/stocks/"), {'get': 'retrieve'}, status.HTTP_403_FORBIDDEN),
        ("Staff user POST", user_staff, request_factory.post("/api/stocks/"), {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Customer user POST", user_customer, request_factory.post("/api/stocks/"),  {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme POST", None, request_factory.post("/api/stocks/"),  {'post': 'create'}, status.HTTP_403_FORBIDDEN),
        ("Staff user PUT", user_staff, request_factory.put("/api/stocks/1", {'reference': 'modified', 'name': 'modified'}), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Customer user PUT", user_customer, request_factory.put("/api/stocks/1"), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme PUT", None, request_factory.put("/api/stocks/1"), {'put': 'update'}, status.HTTP_403_FORBIDDEN),
        ("Staff user DELETE", user_staff, request_factory.delete("/api/stocks/1"), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
        ("Customer user DELETE", user_customer, request_factory.delete("/api/stocks/1"), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
        ("Anonyme DELETE", None, request_factory.delete("/api/stocks/1"), {'delete': 'destroy'}, status.HTTP_403_FORBIDDEN),
    ])
    def test_stock_views_responses(self, _, currentuser, request, view, expected):
        reference_view = StockViewSet.as_view(view)
        if currentuser:
            force_authenticate(request, user=currentuser)
        response = reference_view(request, pk=1)
        self.assertEqual(response.status_code, expected)

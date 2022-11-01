from django.urls import include, path
from rest_framework.routers import DefaultRouter
from beermanagment import views


router = DefaultRouter()
router.register(r'references', views.ReferenceViewSet, basename="reference")
router.register(r'bars', views.BarViewSet, basename="bar")


urlpatterns = [
    path('', views.api_root),
    path('', include(router.urls)),
    path('stocks/', views.StockViewSet.as_view({'get': 'list'}), name='stock-list'),
    path('orders/', views.OrderList.as_view(), name='order-list'),
    path('statistics/', views.statistics, name='statistics'),
]

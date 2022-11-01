from django.urls import include, path
from rest_framework.routers import DefaultRouter
from beermanagment import views


router = DefaultRouter()
router.register(r'references', views.ReferenceViewSet, basename="reference")
router.register(r'bars', views.BarViewSet, basename="bar")


urlpatterns = [
    # path('', views.api_root),
    path('', include(router.urls)),
#     path('references/', views.ReferenceViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# }), name='reference-list'),
#     path('references/<int:pk>/', views.ReferenceViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# }), name='reference-detail'),
#     path('bars/', views.BarViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# }), name='bar-list'),
#     path('bars/<int:pk>/', views.BarViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# }), name='bar-detail'),
    path('stocks/', views.StockViewSet.as_view({'get': 'list'}), name='stock-list'),
    path('orders/', views.OrderList.as_view(), name='order-list'),
    path('statistics/', views.statistics, name='statistics'),
]

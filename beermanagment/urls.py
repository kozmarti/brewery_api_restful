from django.urls import path
from beermanagment import views

urlpatterns = [
	path('', views.api_root),
 	path('references/', views.ReferenceViewSet.as_view({
    'get': 'list',
    'post': 'create'
}), name='reference-list'),
    path('references/<int:pk>/', views.ReferenceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}), name='reference-detail'),
    path('bars/', views.BarViewSet.as_view({
    'get': 'list',
    'post': 'create'
}), name='bar-list'),
    path('bars/<int:pk>/', views.BarViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
}), name='bar-detail'),
    path('stocks/', views.StockViewSet.as_view({
    'get': 'list',
}), name='stock-list'),
    path('orders/', views.OrderList.as_view(), name='order-list'),
    path('statistics/', views.statistics, name='statistics'),
	]
"""brewery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from beermanagment import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/references/', views.ReferenceViewSet.as_view({
    'get': 'list',
    'post': 'create'
})),
    path('api/references/<int:pk>/', views.ReferenceViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})),
    path('api/bars/', views.BarViewSet.as_view({
    'get': 'list',
    'post': 'create'
})),
    path('api/bars/<int:pk>/', views.BarViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})),
    path('api/stocks/', views.StockViewSet.as_view({
    'get': 'list',
})),
    path('api/orders/', views.OrderList.as_view()),
    path('api/orders/<int:pk>/', views.OrderDetail.as_view()),
    path('api/statistics/', views.statistics),
]

from django.urls import path
from . import views
from .views import MyTokenObtainPairView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('', views.getRoutes),
    path('notes/', views.getNotes),
    path('one/', views.getOneNote),
    path('register/', views.register),
    path('orderbook/', views.orderBook),
    path('addbook/', views.addBook),
    path('getallbooks/', views.getAllBooks),
    path('getOrders/', views.getOrders),


    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

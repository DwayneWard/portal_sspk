from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from authority import views

from .views import CustomTokenObtainPairView

urlpatterns = [
    path('users/', views.UsersView.as_view()),
    path('users/create/', views.UserCreateView.as_view()),
    path('users/<int:pk>/', views.UserView.as_view()),
    path('cabinet/', views.CabinetView.as_view()),
    path('login/', CustomTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]

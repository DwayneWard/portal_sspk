from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from authority import views

urlpatterns = [
    path('users/', views.UsersView.as_view()),
    path('users/create/', views.UserCreateView.as_view()),
    path('users/<int:pk>/', views.UserView.as_view()),
    path('cabinet/', views.CabinetView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]

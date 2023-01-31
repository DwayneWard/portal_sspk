from django.urls import path

from eva.isiao import views

urlpatterns = [
    path('gis/', views.GISListView.as_view()),
    path('gis/<int:pk>', views.GISView.as_view()),
    path('gis/create/', views.GISCreateView.as_view()),
    path('indicators/', views.IndicatorsListView.as_view()),
    path('indicators/<int:pk>/', views.IndicatorView.as_view()),
    path('indicators/create/', views.IndicatorCreateView.as_view()),
]

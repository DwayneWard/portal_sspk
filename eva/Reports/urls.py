from django.urls import path

from eva.Reports import views

urlpatterns = [
    path('download_file/<int:report_number>/<str:file_extension>/', views.download_report_file, name='download'),
]

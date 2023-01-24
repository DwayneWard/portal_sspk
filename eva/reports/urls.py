from django.urls import path

from eva.reports import views

urlpatterns = [
    path('download_file/<str:report_number>/<str:file_extension>/', views.download_report_file, name='download'),
    path('', views.ReportsListView.as_view(), name='reports_catalog'),
    path('<str:report_serial_number>/', views.ReportView.as_view(), name='generate_report'),
    path('<str:report_serial_number>/<str:data_format>/', views.ReportView.as_view(), name='report_in_format'),
]

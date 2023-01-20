from django.urls import path

from eva.reports import views

urlpatterns = [
    path('download_file/<int:report_number>/<str:file_extension>/', views.download_report_file, name='download'),
    path('report_catalog/', views.ReportsListView.as_view(), name='report_catalog'),
    path('report/<str:report_serial_number>/', views.ReportView.as_view(), name='report'),
]

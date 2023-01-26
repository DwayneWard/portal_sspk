from django.urls import path

from eva.reports import views

urlpatterns = [
    path('', views.CategoriesWithReportsView.as_view(), name='reports_for_user'),
    path('<str:report_serial_number>/', views.GenerateReportView.as_view(), name='generate_report'),
    path('<str:report_serial_number>/json/', views.ReportAtJsonFormatView.as_view(), name='report_in_json'),
    path('<str:report_serial_number>/<str:file_extension>/', views.download_report_file, name='report_in_file'),
]

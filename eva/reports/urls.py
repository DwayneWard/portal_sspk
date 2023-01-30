from django.urls import path

from eva.reports import views

urlpatterns = [
    path('', views.CategoriesWithReportsView.as_view(), name='reports_for_user'),
    path('create_report/', views.ReportCreateView.as_view(), name='create_new_report'),
    path('<pk>/', views.ReportView.as_view(), name='generate_delete_update_report'),
    path('<pk>/json/', views.ReportAtJsonFormatView.as_view(), name='report_in_json'),
    path('<pk>/<str:file_extension>/', views.DownloadFilesView.as_view(), name='report_in_file'),
]

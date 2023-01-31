from django.urls import path

from eva.reports import views

urlpatterns = [
    path('reports/', views.CategoriesWithReportsView.as_view(), name='reports_for_user'),
    path('reports/create/', views.ReportCreateView.as_view(), name='create_new_report'),
    path('reports/<pk>/', views.ReportView.as_view(), name='generate_delete_update_report'),
    path('reports/<pk>/json/', views.ReportAtJsonFormatView.as_view(), name='report_in_json'),
    path('reports/<pk>/<str:file_extension>/', views.DownloadFilesView.as_view(), name='report_in_file'),
    path('reports_categories/', views.CategoriesListView.as_view(), name='reports_categories'),
    path('reports_categories/create/', views.CategoryCreateView.as_view(), name='reports_category_create'),
    path('reports_categories/<pk>/', views.CategoryView.as_view(), name='reports_category_get_update_delete'),

]

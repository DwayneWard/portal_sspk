from django.urls import path

from control_panel import views

urlpatterns = [
    path('check_results/', views.TasksResultsView.as_view(), name='check_tasks_results'),
    path('resend_tasks/', views.ResendTaskResultView.as_view(), name='resend_tasks'),
]

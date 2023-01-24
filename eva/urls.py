from django.urls import include, path

urlpatterns = [
    path('reports_catalog/', include("eva.reports.urls")),
]

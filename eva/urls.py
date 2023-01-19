from django.urls import include, path

urlpatterns = [
    path('reports/', include("eva.Reports.urls")),
]

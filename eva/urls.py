from django.urls import include, path

urlpatterns = [
    path('reports/', include("Reports.urls")),
]

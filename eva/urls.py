from django.urls import include, path

urlpatterns = [
    path('', include("eva.reports.urls")),
    path('isiao/', include("eva.isiao.urls")),
]

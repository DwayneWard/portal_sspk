from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

from portal import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('apps/', views.ToolsForCurrentUser.as_view()),
    path('eva/', include('eva.urls')),
    # path('auth/', include('authority.urls')),
    path('control_panel/', include('control_panel.urls')),
]

docs_urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/',
         SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += docs_urlpatterns

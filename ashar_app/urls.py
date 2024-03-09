from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

API_TITLE = 'Ashar API'
API_DESCRIPTION = 'Ashar API'
API_VERSION = '1.0.0'


schema_view = get_schema_view(
        openapi.Info(
            title=API_TITLE,
            default_version=API_VERSION,
            description=API_DESCRIPTION,
            ),
        public=True,
        permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('user.urls')),
    path('api/v1/', include('term.urls')),
    path('api/v1/likes/', include('like.urls')),
    path('social-accounts/', include('allauth.urls'), name='socialaccount_signup'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.documentation import include_docs_urls

API_TITLE = 'Ashar API'
API_DESCRIPTION = 'Ashar API'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/accounts/', include('user.urls')),
    path('api/v1/', include('term.urls')),
    path('api/v1/likes/', include('like.urls')),
    # path('docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION)),
    path('social-accounts/', include('allauth.urls'), name='socialaccount_signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

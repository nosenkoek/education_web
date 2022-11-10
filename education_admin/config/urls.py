from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('report/', include('app_report.urls')),
    path('api/', include('app_api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

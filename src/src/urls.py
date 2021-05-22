import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin-old/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

    path('', include('cinema_site.urls')),
    path('', include('profiles.urls')),
    path('admin/', include('admin_lte.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

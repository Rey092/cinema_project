import debug_toolbar
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path('admin-old/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

    path('', include('cinema_site.urls')),
    path('', include('profiles.urls')),
    path('admin/', include('admin_lte.urls')),
]

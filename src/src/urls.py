import debug_toolbar
from decorator_include import decorator_include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import include, path

urlpatterns = [
    path('admin-old/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),

    path('', include('cinema_site.urls')),
    path('', include('profiles.urls')),

    path('admin/', decorator_include(staff_member_required(
        login_url='profiles:login_admin'), 'admin_lte.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

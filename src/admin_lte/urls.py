from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_lte_home, name='admin_lte_home'),
]

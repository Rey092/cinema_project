from django.urls import path

from . import views

urlpatterns = [
    path('', views.admin_lte_home, name='admin_lte_home'),
    path('movies/', views.MoviesView.as_view(), name='movies_list'),
    path('movies/<slug:slug>', views.edit_movie_view, name='movie_description'),
]

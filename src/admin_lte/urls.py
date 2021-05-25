from django.urls import path

from . import views

app_name = 'admin_lte'
urlpatterns = [
    path('', views.admin_lte_home, name='admin_lte_home'),
    path('movies/', views.MoviesView.as_view(), name='movies_list'),
    path('movies/<slug:slug>/', views.movie_description_view, name='movie_description'),

    path('cinemas/', views.CinemasListView.as_view(), name='cinemas_list'),
    path('cinemas/<slug:slug>/', views.cinema_description_view, name='cinema_description'),
    path('cinemas/<slug:slug>/<int:hall_number>', views.hall_description_view, name='hall_description'),
]

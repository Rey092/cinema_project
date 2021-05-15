from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='static/assets/img/favicon/favicon.ico')),

    path('', views.HomePageView.as_view(), name='home_page'),

    path('movies', views.MoviesView.as_view(), name='movies'),
    path('movies/<int:movie_slug>/', views.ConcreteMovieView.as_view(), name='movie'),
    path('movies/soon', views.MoviesSoonView.as_view(), name='movies_soon'),
    path('movies/schedule/', views.ScheduleMovieView.as_view(), name='schedule'),
]

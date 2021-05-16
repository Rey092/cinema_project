from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from . import views

urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='static/assets/img/favicon/favicon.ico')),

    path('', views.HomePageView.as_view(), name='home_page'),

    path('movies', views.MoviesView.as_view(), name='movies_list'),
    path('movies/schedule/', views.MoviesScheduleView.as_view(), name='movies_schedule'),
    path('movies/soon', views.MoviesSoonView.as_view(), name='movies_soon'),

    path('movies/<int:movie_slug>/', views.MovieDescriptionView.as_view(), name='movie_description'),
    path('movies/booking/<int:movie_slug>/', views.MovieBookingView.as_view(), name='movie_booking'),

    path('cinema/list', views.CinemasListView.as_view(), name='cinemas_list'),
    path('cinema/list/<int:cinema_slug>', views.CinemaDescriptionView.as_view(), name='cinema_description'),
    path('cinema/list/<int:cinema_slug>/<int:hall_id>', views.HallDescriptionView.as_view(), name='hall_description'),

    path('events/', views.EventsView.as_view(), name='events_and_discounts'),
    path('events/<int:event_slug>/', views.EventDescriptionView.as_view(), name='event_description'),

    path('about/', views.AboutView.as_view(), name='about'),
    path('news/', views.NewsView.as_view(), name='news'),
    path('pub/', views.PubView.as_view(), name='pub'),
    path('vip-hall/', views.VipHallView.as_view(), name='vip_hall'),
    path('children-room/', views.ChildrenRoomView.as_view(), name='children_room'),
    path('advertisement-info/', views.AdvertisementInfoView.as_view(), name='advertisement_info'),
]

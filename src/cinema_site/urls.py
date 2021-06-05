from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from . import views

app_name = 'cinema_site'
urlpatterns = [
    url(r'^favicon\.ico$', RedirectView.as_view(url='static/assets/img/favicon/favicon.ico')),

    path('', views.HomePageView.as_view(), name='home_page'),

    path('movies/', views.MoviesView.as_view(), name='movies_list'),
    path('movies/schedule/', views.MoviesScheduleView.as_view(), name='movies_schedule'),
    path('movies/<slug:slug>/', views.MovieDescriptionView.as_view(), name='movie_description'),
    path('movies/<slug:slug>/booking/', views.MovieBookingView.as_view(), name='movie_booking'),

    path('cinemas/', views.CinemasListView.as_view(), name='cinemas_list'),
    path('cinemas/<slug:slug>/', views.CinemaDescriptionView.as_view(), name='cinema_description'),
    path('cinemas/<slug:cinema_slug>/<int:hall_id>/', views.HallDescriptionView.as_view(), name='hall_description'),

    path('events/', views.EventsView.as_view(), name='events_and_discounts'),
    path('events/<slug:event_slug>/', views.EventDescriptionView.as_view(), name='event_description'),

    path('news/', views.NewsView.as_view(), name='news'),
    path('news/<slug:news_slug>/', views.NewsDescriptionView.as_view(), name='news_description'),

    path('about/', views.AboutView.as_view(), name='about'),
    path('pub/', views.PubView.as_view(), name='pub'),
    path('vip-hall/', views.VipHallView.as_view(), name='vip_hall'),
    path('children-room/', views.ChildrenRoomView.as_view(), name='children_room'),
    path('advertisement-info/', views.AdvertisementInfoView.as_view(), name='advertisement_info'),
    path('mobile-app-info/', views.MobileAppInfoView.as_view(), name='mobile_app_info'),
    path('contacts/', views.ContactsView.as_view(), name='contacts_view'),
]

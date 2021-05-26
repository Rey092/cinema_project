from django.urls import path

from . import views

app_name = 'admin_lte'
urlpatterns = [
    path('', views.admin_lte_home, name='admin_lte_home'),
    path('movies/', views.MoviesView.as_view(), name='movies_list'),
    path('movies/<slug:slug>/', views.movie_description_view, name='movie_description'),

    path('cinemas/', views.CinemasListView.as_view(), name='cinemas_list'),
    path('cinemas/<slug:slug>/', views.cinema_description_view, name='cinema_description'),
    path('cinemas/<slug:slug>/<int:hall_number>/', views.hall_description_view, name='hall_description'),

    path('news/', views.ArticleListView.as_view(), name='news_list'),
    path('news/create', views.article_create_view, name='news_create'),
    path('news/<slug:slug>/', views.article_description_view, name='news_description'),
    path('news/<slug:slug>/delete/', views.ArticleDeleteView.as_view(), name='news_delete'),

    path('events/', views.ArticleListView.as_view(), name='events_list'),
    path('events/create', views.article_create_view, name='event_create'),
    path('events/<slug:slug>/', views.article_description_view, name='event_description'),
    path('events/<slug:slug>/delete/', views.ArticleDeleteView.as_view(), name='event_delete'),
]

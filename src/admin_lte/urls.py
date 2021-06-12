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

    path('pages/', views.PagesListView.as_view(), name='pages_list'),
    path('pages/create/', views.pages_create_view, name='page_create'),
    path('pages/<slug:slug>/', views.page_description_view, name='page_description'),
    path('pages/<slug:slug>/delete/', views.PageDeleteView.as_view(), name='page_delete'),

    path('contacts/', views.contacts_update_view, name='contacts_list'),
    path('contacts/create/', views.contacts_create_view, name='contacts_create'),

    path('users/', views.UsersListView.as_view(), name='users_list'),
    path('users/<int:pk>/', views.UserUpdateView.as_view(), name='user_description'),
    path('users/<int:pk>/delete', views.UserDeleteView.as_view(), name='user_delete'),

    path('mailings/', views.mailings_view, name='mailings'),
    path('mailings/<int:pk>', views.EmailTemplateDeleteView.as_view(), name='email_template_delete'),

    path('banners/', views.banners_view, name='banners'),
]

from django.urls import path

from . import views

app_name = 'profiles'
urlpatterns = [
    path('user-profile/', views.UserProfileFormView.as_view(), name='user_profile'),

    path('signup/', views.signup_view, name='signup'),

    path('sent/', views.activation_sent_view, name='activation_sent'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]

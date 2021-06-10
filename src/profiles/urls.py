from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'profiles'
urlpatterns = [
    path('profile/', views.UserProfileFormView.as_view(), name='user_profile'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='profiles/pages/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('admin/login', auth_views.LoginView.as_view(
        template_name='profiles/pages/login_admin.html'), name='login_admin'),
    # path('sent/', views.activation_sent_view, name='activation_sent'),
    # path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]

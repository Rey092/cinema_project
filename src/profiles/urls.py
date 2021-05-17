from django.urls import path

from . import views

urlpatterns = [
    path('user-profile/', views.UserProfileFormView.as_view(), name='user_profile'),
]

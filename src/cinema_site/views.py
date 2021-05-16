from django.views.generic import ListView, TemplateView
from profiles.models import UserProfile


class HomePageView(ListView):
    template_name = 'cinema_site/pages/home_page.html'
    queryset = UserProfile


# - Movie Views -

class MoviesView(ListView):
    template_name = 'cinema_site/pages/movies_list.html'
    queryset = UserProfile


class MoviesSoonView(ListView):
    template_name = 'cinema_site/pages/movies_soon.html'
    queryset = UserProfile


class MoviesScheduleView(ListView):
    template_name = 'cinema_site/pages/movies_schedule.html'
    queryset = UserProfile


class MovieDescriptionView(TemplateView):
    template_name = 'cinema_site/pages/movie_description.html'
    queryset = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # movie_slug = context['movie_slug']
        # Movie.objects.filter(movie_slug=movie_slug)
        return context


class MovieBookingView(TemplateView):
    template_name = 'cinema_site/pages/movie_booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # movie_slug = context['movie_slug']
        # Movie.objects.filter(movie_slug=movie_slug)
        return context


# - Cinema Views -

class CinemasListView(ListView):
    template_name = 'cinema_site/pages/cinemas_list.html'
    queryset = UserProfile


class CinemaDescriptionView(TemplateView):
    template_name = 'cinema_site/pages/cinema_description.html'
    queryset = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # movie_slug = context['movie_slug']
        # Movie.objects.filter(movie_slug=movie_slug)
        return context


class HallDescriptionView(TemplateView):
    template_name = 'cinema_site/pages/hall_description.html'
    queryset = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # movie_slug = context['movie_slug']
        # Movie.objects.filter(movie_slug=movie_slug)
        return context


class EventsView(ListView):
    template_name = 'cinema_site/pages/events_and_discounts.html'
    queryset = UserProfile


class EventDescriptionView(ListView):
    template_name = 'cinema_site/pages/event_description.html'
    queryset = UserProfile


class AboutView(ListView):
    template_name = 'cinema_site/pages/about.html'
    queryset = UserProfile


class NewsView(ListView):
    template_name = 'cinema_site/pages/news.html'
    queryset = UserProfile


class PubView(ListView):
    template_name = 'cinema_site/pages/pub.html'
    queryset = UserProfile


class VipHallView(ListView):
    template_name = 'cinema_site/pages/vip_hall.html'
    queryset = UserProfile


class ChildrenRoomView(ListView):
    template_name = 'cinema_site/pages/children_room.html'
    queryset = UserProfile


class AdvertisementInfoView(ListView):
    template_name = 'cinema_site/pages/advertisement_info.html'
    queryset = UserProfile


class MobileAppInfoView(ListView):
    template_name = 'cinema_site/pages/mobile_app_info.html'
    queryset = UserProfile

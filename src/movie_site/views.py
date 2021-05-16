from django.views.generic import ListView, TemplateView
from profiles.models import UserProfile


class HomePageView(ListView):
    template_name = 'movie_site/pages/home_page.html'
    queryset = UserProfile


class MoviesView(ListView):
    template_name = 'movie_site/pages/movies_list.html'
    queryset = UserProfile


class MoviesSoonView(ListView):
    template_name = 'movie_site/pages/movies_soon.html'
    queryset = UserProfile


class MoviesScheduleView(ListView):
    template_name = 'movie_site/pages/movies_schedule.html'
    queryset = UserProfile


class MovieDescriptionView(TemplateView):
    template_name = 'movie_site/pages/movie_description.html'
    queryset = UserProfile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # movie_slug = context['movie_slug']
        # Movie.objects.filter(movie_slug=movie_slug)
        return context


class MovieBookingView(TemplateView):
    template_name = 'movie_site/pages/movie_booking.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # movie_slug = context['movie_slug']
        # Movie.objects.filter(movie_slug=movie_slug)
        return context


class CinemaListView(ListView):
    template_name = 'movie_site/pages/cinema_list.html'
    queryset = UserProfile

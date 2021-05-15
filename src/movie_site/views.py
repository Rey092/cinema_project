from django.shortcuts import render
from django.views.generic import ListView
from profiles.models import UserProfile


class HomePageView(ListView):
    template_name = 'movie_site/pages/home_page.html'
    queryset = UserProfile


class MoviesView(ListView):
    template_name = 'movie_site/pages/movies.html'
    queryset = UserProfile


class MoviesSoonView(ListView):
    template_name = 'movie_site/pages/movies_soon.html'
    queryset = UserProfile


class ScheduleMovieView(ListView):
    template_name = 'movie_site/pages/schedule.html'
    queryset = UserProfile


class ConcreteMovieView(ListView):
    template_name = 'movie_site/pages/concrete_movie.html'
    queryset = UserProfile

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        # form = self.form_class(initial=self.initial)
        context = {}
        return render(request, self.template_name, context=context)

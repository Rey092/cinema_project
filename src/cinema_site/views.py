from datetime import tzinfo, timezone, timedelta
from pprint import pprint

from dateutil.utils import today
from django.core import serializers
from django.http import JsonResponse
from django.utils.datetime_safe import datetime
from django.utils.timezone import utc
from django.views.generic import ListView, TemplateView, UpdateView, DetailView
from cinema_site.models import Movie, Image, Seance, Cinema, Hall
from cinema_site.services.schedule_services import handle_schedule_ajax
from profiles.models import UserProfile


class HomePageView(ListView):
    """View for home page. url: '/'."""

    template_name = 'cinema_site/pages/home_page.html'
    queryset = Movie.objects.filter(is_active=True, release_date__lte=datetime.today())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        movie_list_soon = Movie.objects.filter(is_active=True, release_date__gt=datetime.today())
        today = datetime.today()

        context.update({
            'movie_list_soon': movie_list_soon,
            'today': today
        })
        return context


# - Movie Views -

class MoviesView(ListView):
    """Movies that are now in the cinema. url: 'movies/'."""

    template_name = 'cinema_site/pages/movies_list.html'
    queryset = Movie.objects.filter(is_active=True, release_date__lte=datetime.today())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        movie_list_soon = Movie.objects.filter(is_active=True, release_date__gt=datetime.today())

        context.update({'movie_list_soon': movie_list_soon})
        return context


class MoviesScheduleView(ListView):
    """Movies schedule with movie time and booking. url: 'movies/schedule/'."""

    template_name = 'cinema_site/pages/movies_schedule.html'
    queryset = Seance.objects.select_related('movie', 'hall').filter(time__gt=datetime.now(tz=utc)).order_by('time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cinema_list = Cinema.objects.all()

        context.update({'cinema_list': cinema_list})
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            data = handle_schedule_ajax(request)
            return JsonResponse(data, safe=False, status=200)

        if request.method.lower() in self.http_method_names:
            print(self.http_method_names)
            handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class MovieDescriptionView(DetailView):
    """Single movie description. url: 'movies/<slug:movie_slug>/'."""

    template_name = 'cinema_site/pages/movie_description.html'
    queryset = Movie.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        """Get movie_slug from URL dispatcher, make qs from db and return updated context."""
        context = super().get_context_data(**kwargs)
        movie_url = self.object.trailer_url.split('=')[1]
        images = Image.objects.filter(gallery=self.object.gallery)
        context.update({
            'movie_url': movie_url,
            'images': images,
        })
        return context


class MovieBookingView(TemplateView):
    """Single movie booking. url: 'movies/<slug:movie_slug>/booking/'."""

    template_name = 'cinema_site/pages/movie_booking.html'

    def get_context_data(self, **kwargs):
        """Get movie_slug from URL dispatcher, make qs from db and return updated context."""
        context = super().get_context_data(**kwargs)
        # movie_slug = context['movie_slug']
        # Movie.objects.filter(movie_slug=movie_slug)
        return context


# - Cinema Views -

class CinemasListView(ListView):
    """All cinemas table. url: 'cinemas/'."""

    template_name = 'cinema_site/pages/cinemas_list.html'
    model = Cinema


class CinemaDescriptionView(DetailView):
    """Single cinema description. url: 'cinemas/<slug:cinema_slug>/'."""

    template_name = 'cinema_site/pages/cinema_description.html'
    model = Cinema

    def get_context_data(self, **kwargs):
        """Get movie_slug from URL dispatcher, make qs from db and return updated context."""
        context = super().get_context_data(**kwargs)

        cinema = self.object
        halls = Hall.objects.filter(cinema=cinema)
        tomorrow = today() + timedelta(days=1)

        seances = Seance.objects.select_related('hall').filter(
            time__range=[datetime.now(tz=utc), tomorrow],
            hall__cinema=cinema).order_by('time')

        context.update({'halls': halls, 'seances': seances, })
        return context


class HallDescriptionView(TemplateView):
    """Single hall description. url: 'cinemas/<slug:cinema_slug>/<int:hall_id>/'."""

    template_name = 'cinema_site/pages/hall_description.html'
    queryset = UserProfile

    def get_context_data(self, **kwargs):
        """Get movie_slug from URL dispatcher, make qs from db and return updated context."""
        context = super().get_context_data(**kwargs)
        # movie_slug = context['movie_slug']
        # Movie.objects.filter(movie_slug=movie_slug)
        return context


class EventsView(ListView):
    """All events table. url: 'events/'."""

    template_name = 'cinema_site/pages/events_and_discounts.html'
    queryset = UserProfile


class EventDescriptionView(ListView):
    """Single event description. url: 'events/<slug:event_slug>/'."""

    template_name = 'cinema_site/pages/event_description.html'
    queryset = UserProfile


# - News Views -

class NewsView(ListView):
    """About main cinema. url: 'news/'."""

    template_name = 'cinema_site/pages/news.html'
    queryset = UserProfile


class NewsDescriptionView(ListView):
    """About main cinema. url: 'news/<slug:news_slug>/'."""

    template_name = 'cinema_site/pages/news_description.html'
    queryset = UserProfile


# - Pages Views -

class AboutView(ListView):
    """About main cinema. url: 'about/'."""

    template_name = 'cinema_site/pages/about.html'
    queryset = UserProfile


class PubView(ListView):
    """Pub page. url: 'pub/'."""

    template_name = 'cinema_site/pages/pub.html'
    queryset = UserProfile


class VipHallView(ListView):
    """VIP Hall page. url: 'vip-hall//'."""

    template_name = 'cinema_site/pages/vip_hall.html'
    queryset = UserProfile


class ChildrenRoomView(ListView):
    """Children room page. url: 'children_room/'."""

    template_name = 'cinema_site/pages/children_room.html'
    queryset = UserProfile


class AdvertisementInfoView(ListView):
    """Advertisement info page. url: 'advertisement_info/'."""

    template_name = 'cinema_site/pages/advertisement_info.html'
    queryset = UserProfile


class MobileAppInfoView(ListView):
    """Mobile app page with links (google play, apple store) and info. url: 'mobile-app-info/'."""

    template_name = 'cinema_site/pages/mobile_app_info.html'
    queryset = UserProfile


class ContactsView(ListView):
    """Addresses and locations of cinemas. url: 'contacts_view'."""

    template_name = 'cinema_site/pages/contacts.html'
    queryset = UserProfile

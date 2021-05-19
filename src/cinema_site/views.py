from django.views.generic import ListView, TemplateView
from profiles.models import UserProfile


class HomePageView(ListView):
    """View for home page. url: '/'."""

    template_name = 'cinema_site/pages/home_page.html'
    queryset = UserProfile


# - Movie Views -

class MoviesView(ListView):
    """Movies that are now in the cinema. url: 'movies/'."""

    template_name = 'cinema_site/pages/movies_list.html'
    queryset = UserProfile


class MoviesScheduleView(ListView):
    """Movies schedule with movie time and booking. url: 'movies/schedule/'."""

    template_name = 'cinema_site/pages/movies_schedule.html'
    queryset = UserProfile


class MoviesSoonView(ListView):
    """Movies that will be shown in the cinema soon. url: 'movies/soon/'."""

    # TODO: Возможно, стоит обьеденить MoviesScheduleView и MoviesSoonView в одну вьюшку, когда займусь JS.
    template_name = 'cinema_site/pages/movies_soon.html'
    queryset = UserProfile


class MovieDescriptionView(TemplateView):
    """Single movie description. url: 'movies/<slug:movie_slug>/'."""

    template_name = 'cinema_site/pages/movie_description.html'
    queryset = UserProfile

    def get_context_data(self, **kwargs):
        """Get movie_slug from URL dispatcher, make qs from db and return updated context."""
        context = super().get_context_data(**kwargs)
        # movie_slug = context['movie_slug']
        # Movie.objects.filter(movie_slug=movie_slug)
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
    queryset = UserProfile


class CinemaDescriptionView(TemplateView):
    """Single cinema description. url: 'cinemas/<slug:cinema_slug>/'."""

    template_name = 'cinema_site/pages/cinema_description.html'
    queryset = UserProfile

    def get_context_data(self, **kwargs):
        """Get movie_slug from URL dispatcher, make qs from db and return updated context."""
        context = super().get_context_data(**kwargs)
        # movie_slug = context['movie_slug']
        # Movie.objects.filter(movie_slug=movie_slug)
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

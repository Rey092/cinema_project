import json
from datetime import tzinfo, timezone, timedelta
from pprint import pprint

from dateutil.utils import today
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import JsonResponse, Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from django.utils.decorators import method_decorator
from django.utils.timezone import utc
from django.views.generic import ListView, TemplateView, UpdateView, DetailView
from cinema_site.models import Movie, Image, Seance, Cinema, Hall, Ticket, Article, Page, Contacts, Gallery, \
    BackgroundImage
from cinema_site.services.booking_services import handle_booking_ajax
from cinema_site.services.request_services import get_standard_request_handler
from cinema_site.services.schedule_services import handle_schedule_ajax, localize_datetime_to_rus
from cinema_site.services.standard_page_services import fill_context_for_standard_page_1
from profiles.models import UserProfile
from src.settings import MEDIA_URL


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

        handler = get_standard_request_handler(self, request)
        return handler(request, *args, **kwargs)


class MovieDescriptionView(DetailView):
    """Single movie description. url: 'movies/<slug:movie_slug>/'."""

    template_name = 'cinema_site/pages/movie_description.html'
    queryset = Movie.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        """Get movie_slug from URL dispatcher, make qs from db and return updated context."""
        context = super().get_context_data(**kwargs)
        movie_url = self.object.trailer_url.split('watch?v=')[1]
        images = Image.objects.filter(gallery=self.object.gallery)
        context.update({
            'movie_url': movie_url,
            'images': images,
        })
        return context


@method_decorator(login_required(login_url='/login'), name='dispatch')
class MovieBookingView(DetailView):
    """Single movie booking. url: 'movies/<slug:movie_slug>/booking/'."""

    template_name = 'cinema_site/pages/movie_booking.html'
    queryset = Seance.objects.select_related('movie', 'hall')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        seance_time_rus = localize_datetime_to_rus(self.object.time)
        tickets = Ticket.objects.filter(seance=self.object).values('row', 'seat_place')
        context.update({
            'seance_time': seance_time_rus,
            'tickets': json.dumps(list(tickets)),
            'tickets_count': len(tickets),
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.is_ajax():
            data = handle_booking_ajax(request)
            return JsonResponse(data, safe=False, status=200)

        handler = get_standard_request_handler(self, request)
        return handler(request, *args, **kwargs)


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


def hall_description_view(request, cinema_slug, hall_number):
    cinema = get_object_or_404(Cinema, slug=cinema_slug)
    hall = get_object_or_404(Hall, cinema=cinema, hall_number=hall_number)

    tomorrow = today() + timedelta(days=1)
    seances = Seance.objects.filter(hall=hall, time__range=[datetime.now(tz=utc), tomorrow])
    context = {
        'hall': hall,
        'cinema': cinema,
        'seances': seances,
    }
    return render(request, 'cinema_site/pages/hall_description.html', context=context)


class EventsView(ListView):
    """All events table. url: 'events/'."""

    template_name = 'cinema_site/pages/events_and_discounts.html'
    queryset = Article.objects.filter(mode='EVENTS')


class EventDescriptionView(DetailView):
    """Single event description. url: 'events/<slug:event_slug>/'."""

    template_name = 'cinema_site/pages/article_description.html'
    queryset = Article.objects.filter(mode='EVENTS')

    def get_context_data(self, **kwargs):
        """Get event_slug from URL dispatcher, make qs from db and return updated context."""
        context = super().get_context_data(**kwargs)
        event_url = self.object.trailer_url.split('=')[1]
        images = Image.objects.filter(gallery=self.object.gallery)
        context.update({
            'event_url': event_url,
            'images': images,
        })
        return context

# - News Views -


class NewsView(ListView):
    """About main cinema. url: 'news/'."""

    template_name = 'cinema_site/pages/news.html'
    queryset = Article.objects.filter(mode='NEWS')


class NewsDescriptionView(DetailView):
    """About main cinema. url: 'news/<slug:news_slug>/'."""

    template_name = 'cinema_site/pages/article_description.html'
    queryset = Article.objects.filter(mode='NEWS')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        event_url = self.object.trailer_url.split('=')[1]
        images = Image.objects.filter(gallery=self.object.gallery)
        context.update({
            'event_url': event_url,
            'images': images,
        })
        return context


# - Pages Views -

class AboutView(TemplateView):
    """About main cinema. url: 'about/'."""

    template_name = 'cinema_site/pages/standard_page_1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fill_context_for_standard_page_1(context, 'О кинотеатре')
        return context


class PubView(TemplateView):
    """Pub page. url: 'pub/'."""

    template_name = 'cinema_site/pages/standard_page_1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fill_context_for_standard_page_1(context, 'Кафе-Бар')
        return context


class VipHallView(TemplateView):
    """VIP Hall page. url: 'vip-hall/'."""

    template_name = 'cinema_site/pages/standard_page_1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fill_context_for_standard_page_1(context, 'Vip-Зал')
        return context


class ChildrenRoomView(TemplateView):
    """Children room page. url: 'children_room/'."""

    template_name = 'cinema_site/pages/standard_page_1.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        fill_context_for_standard_page_1(context, 'Детская комната')
        return context


class AdvertisementInfoView(TemplateView):
    """Advertisement info page. url: 'advertisement_info/'."""

    template_name = 'cinema_site/pages/standard_page_1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fill_context_for_standard_page_1(context, 'Реклама')
        return context


class MobileAppInfoView(TemplateView):
    """Mobile app page with links (google play, apple store) and info. url: 'mobile-app-info/'."""

    template_name = 'cinema_site/pages/standard_page_1.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fill_context_for_standard_page_1(context, 'Мобильное приложение')
        return context


class ContactsView(TemplateView):
    """Addresses and locations of cinemas. url: 'contacts_view'."""

    template_name = 'cinema_site/pages/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        contacts = Contacts.objects.filter(is_active=True)
        context.update({'contacts': contacts, })
        return context


def api_banners(request):
    if request.is_ajax():
        try:
            gallery_inst = get_object_or_404(Gallery, name='top_banners_gallery')
        except Http404:
            gallery_inst = Gallery(name='top_banners_gallery')
            gallery_inst.save()
        images = list(Image.objects.filter(gallery=gallery_inst).values_list('image', flat=True))
        banners_data, _ = BackgroundImage.objects.get_or_create(name='background_image')
        carousel_status = banners_data.top_banners_is_active
        if banners_data.image:
            banner = banners_data.image.url
        else:
            banner = 'https://i.pinimg.com/originals/ae/8a/c2/ae8ac2fa217d23aadcc913989fcc34a2.png'
        bg_format = banners_data.bg_format

        return JsonResponse({'images': images, 'carousel_status': carousel_status,
                             'banner': banner, 'bg_format': bg_format}, status=200)
    return Http404


def search_view(request):
    search = request.GET.get('q')
    if search:
        qs = Movie.objects.filter(is_active=True)
        for movie in qs:
            if search.lower() in movie.title.lower():
                return redirect('cinema_site:movie_description', slug=movie.slug)
    else:
        return redirect('cinema_site:home_page')

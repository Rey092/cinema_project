import json
from datetime import timedelta
from pprint import pprint

from dateutil.utils import today
from django.core.mail import send_mail
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count
from django.forms import modelformset_factory
from django.http import Http404, JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.timezone import utc
from cinema_site.models import Cinema, Hall, Movie, Article, Page, Contacts, Gallery, Image, Seance, Logger, \
    EmailTemplate, BackgroundImage
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DeleteView, UpdateView
from cinema_site.services.schedule_services import localize_datetime_to_rus
from profiles.forms import UserProfileFormRestricted
from profiles.models import UserProfile
from admin_lte.services.forms_services import create_forms, get_objects, save_forms, \
    save_new_images_to_gallery, validate_forms, create_objects, save_objects, get_url_path, get_article_qs

from .forms import CinemaForm, HallForm, MovieForm, SeoDataForm, ArticleForm, PageForm, RestrictedPageForm, \
    ContactsForm, MailingForm, ImageForm, BackgroundImageForm
from .tasks import send_emails_from_admin


def admin_lte_home(request):
    users = UserProfile.objects.filter(is_staff=False)
    users_count = users.count()
    men_count = users.filter(gender='M').count()
    women_count = users.filter(gender='F').count()

    seance_data = []
    days = 8
    week_more = today(tzinfo=utc) + timedelta(days=days)
    seances = Seance.objects.filter(time__range=[datetime.now(tz=utc), week_more])

    for i in range(days):
        date = today(tzinfo=utc) + timedelta(days=i)
        next_day = today(tzinfo=utc) + timedelta(days=(i + 1))
        seance_data.append({
            'date': localize_datetime_to_rus(date, time_format='dateMonth'),
            'seance_count': seances.filter(time__range=[date, next_day]).count(),
        })
    seance_data_json = json.dumps(seance_data)

    logs = Logger.objects.values('referer').exclude(referer=None).annotate(the_count=Count('referer')) \
        .order_by('-the_count')
    logs_data_json = json.dumps(list(logs[0:5]))

    context = {
        'users_count': users_count,
        'men_count': men_count,
        'women_count': women_count,
        'seances': seances,
        'seance_data': seance_data_json,
        'logs_data_json': logs_data_json,
    }
    return render(request, 'admin_lte/pages/home.html', context=context)


class MoviesView(ListView):
    template_name = 'admin_lte/pages/movies_list.html'

    def get_queryset(self):
        data = Movie.objects.filter(is_active=True)
        movies_now = data.filter(release_date__lte=datetime.today())
        movies_soon = data.filter(release_date__gt=datetime.today())
        queryset = {
            'now': movies_now,
            'soon': movies_soon,
        }
        return queryset


class MovieDeleteView(DeleteView):
    success_url = reverse_lazy('admin_lte:movies_list')
    model = Movie

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def movie_description_view(request, slug):
    movie, gallery, video_url = get_objects(Movie, slug)
    movie_form, seo_data_form, formset = create_forms(movie, MovieForm, gallery, request)

    if request.method == 'POST':
        forms_valid_status = validate_forms(movie_form, seo_data_form, formset=formset)

        if forms_valid_status:
            save_forms(movie_form, seo_data_form, formset)
            save_new_images_to_gallery(movie, request)

            return redirect('admin_lte:movies_list')

    return render(request, 'admin_lte/pages/movie_description.html',
                  context={'movie': movie, 'form1': movie_form, 'form2': seo_data_form, 'formset': formset})


def movie_create_view(request):
    movie, gallery_images, gallery_inst, seo_inst = create_objects(Movie)
    # movie_form, seo_data_form, formset = create_forms(movie, MovieForm, gallery_images, request)

    formset_factory = modelformset_factory(Image, form=ImageForm, fields={'image', }, extra=0)
    movie_form = MovieForm(request.POST or None, request.FILES or None, prefix='form1', instance=movie)
    seo_data_form = SeoDataForm(request.POST or None, prefix='form2', instance=movie.seo)
    formset = formset_factory(request.POST or None, request.FILES or None, prefix='formset', queryset=gallery_images)

    if request.method == 'POST':
        forms_valid_status = validate_forms(movie_form, seo_data_form, formset=formset)
        if forms_valid_status:
            save_objects(seo_inst, gallery_inst, movie)
            save_forms(movie_form, seo_data_form, formset)
            save_new_images_to_gallery(movie, request)

            return redirect('admin_lte:movies_list')

    return render(request, 'admin_lte/pages/movie_create.html',
                  context={'form1': movie_form, 'form2': seo_data_form, 'formset': formset})


class CinemasListView(ListView):
    """All cinemas table. url: 'admin/cinemas/'."""

    template_name = 'admin_lte/pages/cinemas_list.html'
    model = Cinema


def cinema_description_view(request, slug):
    cinema, gallery = get_objects(Cinema, slug, trailer=False)
    halls = Hall.objects.filter(cinema=cinema)

    cinema_form, seo_data_form, formset = create_forms(cinema, CinemaForm, gallery, request)

    if request.method == 'POST':
        forms_valid_status = validate_forms(cinema_form, seo_data_form, formset=formset)

        if forms_valid_status:
            save_forms(cinema_form, seo_data_form, formset)
            save_new_images_to_gallery(cinema, request)

            return redirect('admin_lte:cinemas_list')

    return render(request, 'admin_lte/pages/cinema_description.html',
                  context={'cinema': cinema, 'form1': cinema_form, 'form2': seo_data_form, 'formset': formset,
                           'halls': halls})


class CinemaDeleteView(DeleteView):
    success_url = reverse_lazy('admin_lte:cinemas_list')
    model = Cinema

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def cinema_create_view(request):
    cinema, gallery_images, gallery_inst, seo_inst = create_objects(Cinema)
    cinema_form, seo_data_form, formset = create_forms(cinema, CinemaForm, gallery_images, request)

    if request.method == 'POST':
        forms_valid_status = validate_forms(cinema_form, seo_data_form, formset=formset)
        if forms_valid_status:
            save_objects(seo_inst, gallery_inst, cinema)
            save_forms(cinema_form, seo_data_form, formset)
            save_new_images_to_gallery(cinema, request)

            return redirect('admin_lte:cinemas_list')

    return render(request, 'admin_lte/pages/cinema_create.html',
                  context={'form1': cinema_form, 'form2': seo_data_form, 'formset': formset})


def hall_create_view(request, slug):
    hall, gallery_images, gallery_inst, seo_inst = create_objects(Hall, slug=slug)
    hall_form, seo_data_form, formset = create_forms(hall, HallForm, gallery_images, request)

    if request.method == 'POST':
        forms_valid_status = validate_forms(hall_form, seo_data_form, formset=formset)
        print(forms_valid_status)
        if forms_valid_status:
            save_objects(seo_inst, gallery_inst, hall)
            save_forms(hall_form, seo_data_form, formset)
            save_new_images_to_gallery(hall, request)

            return redirect('admin_lte:cinema_description', slug=slug)

    return render(request, 'admin_lte/pages/hall_create.html',
                  context={'form1': hall_form, 'form2': seo_data_form, 'formset': formset})


class HallDeleteView(DeleteView):
    success_url = reverse_lazy('admin_lte:cinemas_list')
    model = Hall

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


def hall_description_view(request, slug, hall_number):
    cinema = get_object_or_404(Cinema, slug=slug)
    hall = get_object_or_404(Hall, cinema=cinema, hall_number=hall_number)
    gallery = Image.objects.filter(gallery=hall.gallery)

    hall_form, seo_data_form, formset = create_forms(hall, HallForm, gallery, request)

    if request.method == 'POST':

        forms_valid_status = validate_forms(hall_form, seo_data_form, formset=formset)

        if forms_valid_status:
            save_forms(hall_form, seo_data_form, formset)
            save_new_images_to_gallery(hall, request)

            return redirect('admin_lte:hall_description', slug=slug, hall_number=hall_number)

    return render(request, 'admin_lte/pages/hall_description.html',
                  context={'hall': hall, 'form1': hall_form, 'form2': seo_data_form, 'formset': formset})
# '


class ArticleListView(ListView):
    template_name = 'admin_lte/pages/articles_list.html'

    def get_queryset(self):
        path = get_url_path(self)
        if path == '/admin/news/':
            return get_article_qs('NEWS')
        elif path == '/admin/events/':
            return get_article_qs('EVENTS')


def article_description_view(request, slug):
    article, gallery, video_url = get_objects(Article, slug)
    news_form, seo_data_form, formset = create_forms(article, ArticleForm, gallery, request)

    if request.method == 'POST':
        forms_valid_status = validate_forms(news_form, seo_data_form, formset=formset)

        if forms_valid_status:
            save_forms(news_form, seo_data_form, formset)
            save_new_images_to_gallery(article, request)

            return redirect('admin_lte:news_list')

    return render(request, 'admin_lte/pages/article_description.html',
                  context={'article': article, 'form1': news_form, 'form2': seo_data_form, 'formset': formset,
                           'video_url': video_url})


class ArticleDeleteView(DeleteView):
    model = Article

    def get_success_url(self):
        mode = self.object.mode
        if mode == 'NEWS':
            return reverse_lazy('admin_lte:news_list')
        elif mode == 'EVENTS':
            return reverse_lazy('admin_lte:events_list')


def article_create_view(request):
    mode = 'NEWS' if request.path == '/admin/news/create' else 'EVENTS'
    article, gallery_images, gallery_inst, seo_inst = create_objects(Article, mode)
    article_form, seo_data_form, formset = create_forms(article, ArticleForm, gallery_images, request)

    if request.method == 'POST':
        forms_valid_status = validate_forms(article_form, seo_data_form, formset=formset)

        if forms_valid_status:
            save_objects(seo_inst, gallery_inst, article)
            save_forms(article_form, seo_data_form, formset)
            save_new_images_to_gallery(article, request)
            if mode == 'NEWS':
                return redirect('admin_lte:news_list')
            else:
                return redirect('admin_lte:events_list')
    else:
        seo_data_form = SeoDataForm(prefix='form2', instance=article.seo)

    return render(request, 'admin_lte/pages/article_create.html',
                  context={'form1': article_form, 'form2': seo_data_form, 'formset': formset})


# --------- Pages -----------


class PagesListView(ListView):
    template_name = 'admin_lte/pages/pages_list.html'
    queryset = Page.objects.all().order_by('created')


def page_description_view(request, slug):
    page, gallery = get_objects(Page, slug, trailer=False)

    page_form = RestrictedPageForm if page.is_basic is True else PageForm
    print(page.is_basic)
    page_form, seo_data_form, formset = create_forms(page, page_form, gallery, request)

    if request.method == 'POST':
        forms_valid_status = validate_forms(page_form, seo_data_form, formset=formset)

        if forms_valid_status:
            save_forms(page_form, seo_data_form, formset)
            save_new_images_to_gallery(page, request)

            return redirect('admin_lte:pages_list')

    return render(request, 'admin_lte/pages/page_description.html',
                  context={'page': page, 'form1': page_form, 'form2': seo_data_form, 'formset': formset})


class PageDeleteView(DeleteView):
    success_url = reverse_lazy('admin_lte:pages_list')
    model = Page


def pages_create_view(request):
    page, gallery_images, gallery_inst, seo_inst = create_objects(Page)
    article_form, seo_data_form, formset = create_forms(page, PageForm, gallery_images, request)

    if request.method == 'POST':
        forms_valid_status = validate_forms(article_form, seo_data_form, formset=formset)

        if forms_valid_status:
            save_objects(seo_inst, gallery_inst, page)
            save_forms(article_form, seo_data_form, formset)
            save_new_images_to_gallery(page, request)

            return redirect('admin_lte:pages_list')

    return render(request, 'admin_lte/pages/page_create.html',
                  context={'form1': article_form, 'form2': seo_data_form, 'formset': formset})


def contacts_update_view(request):
    qs = Contacts.objects.all()
    forms = [ContactsForm(request.POST or None, request.FILES or None, prefix=f'form{x.id}', instance=x) for x in qs]

    if request.method == 'POST':
        forms_valid_status = validate_forms(*forms)

        if forms_valid_status:
            save_forms(*forms)

        return redirect('admin_lte:pages_list')

    return render(request, 'admin_lte/pages/contacts_update.html', context={'forms': forms})


def contacts_create_view(request):
    form = ContactsForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        forms_valid_status = validate_forms(form)

        if forms_valid_status:
            save_objects(form)

            return redirect('admin_lte:pages_list')

    return render(request, 'admin_lte/pages/contacts_create.html', context={'form': form})


# --------- Users ------------

class UsersListView(ListView):
    template_name = 'admin_lte/pages/users_list.html'
    model = UserProfile


class UserUpdateView(UpdateView):
    model = UserProfile
    template_name = 'admin_lte/pages/user_update_view.html'
    form_class = UserProfileFormRestricted
    success_message = 'Success'
    success_url = reverse_lazy('admin_lte:users_list')

    def form_valid(self, form):
        new_password = form.cleaned_data.get('new_password')
        confirm_password = form.cleaned_data.get('confirm_password')

        if new_password == confirm_password and new_password:
            self.object.set_password(new_password)
            self.object.save()
            return redirect(reverse('admin_lte:users_list'))

        return super().form_valid(form)


class UserDeleteView(DeleteView):
    success_url = reverse_lazy('admin_lte:users_list')
    model = UserProfile


def mailings_view(request):
    if request.is_ajax():
        text = request.POST['text']
        choice_type = request.POST['choice_type']
        users_id_list = request.POST['users_id_list'].split(',')
        template_choice = request.POST['template_choice']

        if template_choice == 'newTemplate':
            files = request.FILES
            template = EmailTemplate(file=files.get('html_file', None))
            template.save()
        else:
            template = get_object_or_404(EmailTemplate, pk=template_choice)
        template_id = str(template.id)

        if choice_type == 'choice_all':
            users = UserProfile.objects.filter(is_active=True)
            emails = list(users.values_list('email', flat=True))
            send_emails_from_admin.delay(emails, template_id, text)
        elif choice_type == 'choice_selected':
            users = UserProfile.objects.filter(is_active=True, pk__in=users_id_list)
            emails = list(users.values_list('email', flat=True))
            send_emails_from_admin.delay(emails, template_id, text)
        else:
            return JsonResponse({'status': 'error, invalid form data'}, safe=False, status=500)

        return JsonResponse({'status': 'success'}, safe=False, status=200)

    mailing_form = MailingForm()
    users_list = UserProfile.objects.all()
    users_number = users_list.count()
    templates_list = EmailTemplate.objects.all().order_by('-id')[:5][::-1]
    context = {
        'mailing_form': mailing_form,
        'users_list': users_list,
        'users_number': users_number,
        'templates_list': templates_list
    }
    return render(request, 'admin_lte/pages/mailing.html', context=context)


class EmailTemplateDeleteView(DeleteView):
    success_url = reverse_lazy('admin_lte:mailings')
    model = EmailTemplate


def banners_view(request):
    gallery_inst, _ = Gallery.objects.get_or_create(name='top_banners_gallery')
    background_image, _ = BackgroundImage.objects.get_or_create(name='background_image')
    image_form = BackgroundImageForm(request.POST or None, request.FILES or None, prefix='image_form',
                                     instance=background_image)

    gallery = Image.objects.filter(gallery=gallery_inst)
    formset_factory = modelformset_factory(Image, form=ImageForm, fields={'image', }, extra=0)
    formset = formset_factory(request.POST or None, request.FILES or None, prefix='formset', queryset=gallery)

    if request.method == 'POST':
        forms_valid_status = validate_forms(image_form, formset=formset)

        if forms_valid_status:
            save_objects(background_image)
            save_forms(image_form, formset)
            save_new_images_to_gallery(None, request, gallery=gallery_inst)

            return redirect('admin_lte:banners')

    context = {
        'formset': formset,
        'image_form': image_form,
        'current_image': background_image
    }

    return render(request, 'admin_lte/pages/banners_list.html', context=context)


class BackgroundImageDeleteView(DeleteView):
    success_url = reverse_lazy('admin_lte:banners')
    model = BackgroundImage

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class BannerDeleteView(DeleteView):
    success_url = reverse_lazy('admin_lte:banners')
    model = Image

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

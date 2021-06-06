from django.forms import modelformset_factory
from django.http import Http404
from django.urls import reverse_lazy, reverse
from cinema_site.models import Cinema, Hall, Movie, Article, Page, Contacts, Gallery, Image
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.datetime_safe import datetime
from django.views.generic import ListView, DeleteView, UpdateView
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from admin_lte.services.forms_services import create_forms, get_objects, save_forms, \
    save_new_images_to_gallery, validate_forms, create_objects, save_objects, get_url_path, get_article_qs

from .forms import CinemaForm, HallForm, MovieForm, SeoDataForm, ArticleForm, PageForm, RestrictedPageForm, \
    ContactsForm, MailingForm, ImageForm


def admin_lte_home(request):
    users = UserProfile.objects.filter(is_staff=False)
    users_count = users.count()
    men_count = users.filter(gender='M').count()
    women_count = users.filter(gender='F').count()
    context = {
        'users_count': users_count,
        'men_count': men_count,
        'women_count': women_count,
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


def hall_description_view(request, slug, hall_number):
    cinema, gallery = get_objects(Cinema, slug, trailer=False)
    hall = get_object_or_404(Hall, cinema=cinema, hall_number=hall_number)

    hall_form, seo_data_form, formset = create_forms(hall, HallForm, gallery, request)

    if request.method == 'POST':
        forms_valid_status = validate_forms(hall_form, seo_data_form, formset=formset)

        if forms_valid_status:
            save_forms(hall_form, seo_data_form, formset)
            save_new_images_to_gallery(hall, request)

            return redirect('admin_lte:hall_description', slug=cinema.slug, hall_number=hall.hall_number)

    return render(request, 'admin_lte/pages/hall_description.html',
                  context={'hall': hall, 'form1': hall_form, 'form2': seo_data_form, 'formset': formset})


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
    form_class = UserProfileForm
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
    mailing_form = MailingForm()
    return render(request, 'admin_lte/pages/mailing.html', context={'mailing_form': mailing_form})


def banners_view(request):
    try:
        gallery_inst = get_object_or_404(Gallery, name='top_banners_gallery')
    except Http404:
        gallery_inst = Gallery(name='top_banners_gallery')
        gallery_inst.save()

    gallery = Image.objects.filter(gallery=gallery_inst)
    formset_factory = modelformset_factory(Image, form=ImageForm, fields={'image', }, extra=0)
    formset = formset_factory(request.POST or None, request.FILES or None, prefix='formset', queryset=gallery)

    if request.method == 'POST':
        forms_valid_status = validate_forms(formset=formset)

        if forms_valid_status:
            save_forms(formset)
            save_new_images_to_gallery(None, request, gallery=gallery_inst)

            return redirect('admin_lte:banners')

    return render(request, 'admin_lte/pages/banners_list.html', context={'formset': formset})

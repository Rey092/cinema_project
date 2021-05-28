from django.forms import modelformset_factory, formset_factory
from django.urls import reverse_lazy
from cinema_site.models import Cinema, Hall, Movie, Article, Gallery, SeoData, Image, Page, Contacts
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.datetime_safe import datetime, date
from django.views.generic import ListView, DeleteView, CreateView, UpdateView

from .forms import CinemaForm, HallForm, MovieForm, SeoDataForm, ArticleForm, ImageForm, PageForm, RestrictedPageForm, \
    ContactsForm
from .templates.admin_lte.services.forms_services import create_forms, get_objects, save_forms, \
    save_new_images_to_gallery, validate_forms, create_objects, save_objects, get_url_path, get_article_qs


def admin_lte_home(request):
    return render(request, 'admin_lte/pages/home.html')


class MoviesView(ListView):
    """Movies that are in the cinema now or soon will be. url: 'movies/'. TODO."""

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
    model = Page


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
    else:
        seo_data_form = SeoDataForm(prefix='form2', instance=page.seo)

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

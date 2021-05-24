from cinema_site.models import Cinema, Hall, Image, Movie, MovieGalleryImage
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.datetime_safe import datetime
from django.views.generic import ListView

from .forms import CinemaForm, ImageForm, MovieForm, MovieGalleryImageForm, PosterForm, SeoDataForm


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
    movie = get_object_or_404(Movie, slug=slug)
    formset_factory = modelformset_factory(MovieGalleryImage, form=MovieGalleryImageForm, extra=0, max_num=6)
    gallery = MovieGalleryImage.objects.filter(movie=movie)

    if request.method == 'POST':
        movie_form = MovieForm(request.POST, prefix='form1', instance=movie)
        seo_data_form = SeoDataForm(request.POST, prefix='form2', instance=movie.seo)
        poster_form = PosterForm(request.POST, request.FILES, prefix='poster_form')
        formset = formset_factory(request.POST, request.FILES, prefix='formset')

        valid1 = movie_form.is_valid()
        valid2 = seo_data_form.is_valid()
        valid3 = poster_form.is_valid()
        valid4 = formset.is_valid()

        if all([valid1, valid2, valid3, valid4]):
            movie_form.save(commit=True)
            seo_data_form.save(commit=True)

            formset.save(commit=True)

            undefined_images = request.FILES.getlist('formset-undefined-image')
            for image in undefined_images:
                print(undefined_images)
                gallery_image = MovieGalleryImage(image=image, movie=movie)
                gallery_image.save()

            if request.FILES.get('poster_form-picture'):
                poster = get_object_or_404(Image, id=movie.poster.id)
                poster.image = request.FILES.get('poster_form-picture')
                poster.save()

            return redirect('movies_list')

    movie_form = MovieForm(instance=movie, prefix='form1')
    seo_data_form = SeoDataForm(instance=movie.seo, prefix='form2')
    poster_form = PosterForm(prefix='poster_form')
    formset = formset_factory(queryset=gallery, prefix='formset')

    return render(request, 'admin_lte/pages/movie_description.html',
                  context={'movie': movie, 'form1': movie_form, 'form2': seo_data_form, 'poster_form': poster_form,
                           'formset': formset})


class CinemasListView(ListView):
    """All cinemas table. url: 'admin/cinemas/'."""

    template_name = 'admin_lte/pages/cinemas_list.html'
    model = Cinema


def cinema_description_view(request, slug):
    cinema = get_object_or_404(Cinema, slug=slug)
    formset_factory = modelformset_factory(Image, form=ImageForm, fields={'image', }, extra=0, max_num=6)
    gallery = Image.objects.filter(gallery=cinema.gallery)

    if request.method == 'POST':
        cinema_form = CinemaForm(request.POST, request.FILES, prefix='form1', instance=cinema)
        seo_data_form = SeoDataForm(request.POST, prefix='form2', instance=cinema.seo)
        formset = formset_factory(request.POST, request.FILES, prefix='formset')

        valid1 = cinema_form.is_valid()
        valid2 = seo_data_form.is_valid()
        valid3 = formset.is_valid()

        if all([valid1, valid2, valid3]):
            cinema_form.save(commit=True)
            seo_data_form.save(commit=True)

            formset.save(commit=True)

            undefined_images = request.FILES.getlist('formset-undefined-image')
            for image in undefined_images:
                gallery_image = Image(image=image, gallery=cinema.gallery)
                gallery_image.save()

            return redirect('cinemas_list')

    cinema_form = CinemaForm(instance=cinema, prefix='form1')
    seo_data_form = SeoDataForm(instance=cinema.seo, prefix='form2')
    formset = formset_factory(queryset=gallery, prefix='formset')
    halls = Hall.objects.filter(cinema=cinema)

    return render(request, 'admin_lte/pages/cinema_description.html',
                  context={'cinema': cinema, 'form1': cinema_form, 'form2': seo_data_form, 'formset': formset,
                           'halls': halls})

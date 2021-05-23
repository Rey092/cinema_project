from cinema_site.models import Image, Movie, MovieGalleryImage, SeoData
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.datetime_safe import datetime
from django.views.generic import ListView

from .forms import MovieForm, MovieGalleryImageForm, PosterForm, SeoDataForm


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


def edit_movie_view(request, slug):
    movie = get_object_or_404(Movie, slug=slug)
    seo = get_object_or_404(SeoData, id=movie.seo.id)
    gallery_form_set = modelformset_factory(MovieGalleryImage, form=MovieGalleryImageForm, extra=0, max_num=6)
    gallery = MovieGalleryImage.objects.filter(movie=movie)

    if request.method == 'POST':
        movie_form = MovieForm(request.POST, prefix='form1', instance=movie)
        seo_data_form = SeoDataForm(request.POST, prefix='form2', instance=seo)
        poster_form = PosterForm(request.POST, request.FILES, prefix='poster_form')
        formset = gallery_form_set(request.POST, request.FILES, prefix='formset')

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
    seo_data_form = SeoDataForm(instance=seo, prefix='form2')
    poster_form = PosterForm(prefix='poster_form')
    formset = gallery_form_set(queryset=gallery, prefix='formset')

    return render(request, 'admin_lte/pages/movie_description.html',
                  context={'movie': movie, 'form1': movie_form, 'form2': seo_data_form, 'poster_form': poster_form,
                           'formset': formset})

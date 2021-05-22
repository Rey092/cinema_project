from cinema_site.models import Movie, MovieGallery, SeoData
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.datetime_safe import datetime
from django.views.generic import ListView

from .forms import MovieForm, MovieGalleryForm, SeoDataForm


def admin_lte_home(request):
    return render(request, 'admin_lte/pages/home.html')


class MoviesView(ListView):
    """Movies that are now in the cinema. url: 'movies/'. TODO."""

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
    gallery = MovieGallery.objects.filter(movie=movie)
    print(1)

    if request.method == 'POST':
        print(2)
        movie_form = MovieForm(request.POST, prefix='form1', instance=movie)
        print(movie_form.is_valid(), movie_form.errors, movie_form.non_field_errors())
        seo_data_form = SeoDataForm(request.POST, prefix='form2', instance=seo)
        # gallery_forms = [MovieGalleryForm(request.POST, request.FILES, instance=x, prefix=f'gallery1') for x in
        # gallery]

        valid1 = movie_form.is_valid()
        valid2 = seo_data_form.is_valid()
        valid3 = True
        # for gallery in gallery_forms:
        #     if not gallery.is_valid():
        #         valid3 = False
        print(valid1, valid2, valid3)
        if valid1 and valid2 and valid3:
            print(4)
            movie_form.save(commit=True)
            seo_data_form.save(commit=True)
            # print(gallery_forms)
            print(5)
            return redirect('movies_list')

    gallery_forms = [MovieGalleryForm(instance=x, prefix='gallery') for x in gallery]
    movie_form = MovieForm(instance=movie, prefix='form1')
    seo_data_form = SeoDataForm(instance=seo, prefix='form2')
    return render(request, 'admin_lte/pages/movie_description.html',
                  context={'movie': movie, 'form1': movie_form, 'form2': seo_data_form, 'gallery_forms': gallery_forms,
                           'gallery': gallery})

# class MovieDescriptionView(SuccessMessageMixin, UpdateView):
#     """Movies that are now in the cinema. url: 'movies/'. TODO"""
#     template_name = 'admin_lte/pages/movie_description.html'
#     model = Movie
#     form_class = MovieForm
#     form_class2 = SeoDataForm
#     success_message = 'Success'
#     success_url = reverse_lazy('movies_list')
#
#     # def get_context_data(self, **kwargs):
#     #     context = super(MovieDescriptionView, self).get_context_data(**kwargs)
#     #     context['form2'] = self.form_class2(instance=self.object.seo)
#     #     return context
#
#     def get_context_data(self, **kwargs):
#
#         context = super(MovieDescriptionView, self).get_context_data(**kwargs)
#         context['form2'] = self.form_class2(instance=self.object.seo)
#         context['form2'] = inlineformset_factory(SeoData, Movie, form=MovieForm, fields=('title', 'slug'))
#         return context

# def get_object(self, queryset=None):
#     if queryset is None:
#         queryset = self.get_queryset()
#
#     pk = self.kwargs.get(self.pk_url_kwarg)
#     slug = self.kwargs.get(self.slug_url_kwarg)
#
#     if pk is not None:
#         queryset = queryset.filter(pk=pk)
#
#     if slug is not None and (pk is None or self.query_pk_and_slug):
#         slug_field = self.get_slug_field()
#         queryset = queryset.filter(**{slug_field: slug})
#
#     if pk is None and slug is None:
#         raise Http404()
#     try:
#         obj = queryset.get()
#     except queryset.model.DoesNotExist:
#         raise Http404()
#
#     return obj
#
# def form_invalid(self, **kwargs):
#     return self.render_to_response(self.get_context_data(**kwargs))
#
# def post(self, request, *args, **kwargs):
#     self.object = self.get_object()
#
#     form = MovieForm(request.POST, prefix='form')
#     if form.is_valid():
#         form.save()
#     return reverse('admin_lte_home')


# def post(self, request, *args, **kwargs):
#     self.object = self.get_object()
#
#     if not request.user.is_authenticated:
#         return HttpResponseForbidden
#
#     form1 = MovieForm(request.POST)
#     form2 = SeoDataForm(request.POST)
#
#     f1_valid = form1.is_valid()
#     f2_valid = form2.is_valid()
#     if f1_valid or f2_valid:
#         print('go')
#         form2.save()
#         # form2.save()
#         # form2.save()
#         # new_form = Movie()
#         # newdoc.save()
#
#         # Redirect to the document list after POST
#     return reverse('movies_list')

# if form.is_valid():
#     return self.form_valid(form)
# else:
#     return self.form_invalid(form)

# def form_valid(self, form):
#     current_task = get_object_or_404(Movie, slug=self.kwargs['slug'])
#     self.object = form.save(commit=False)
#     self.object.task = current_task
#     self.object.save()
#     return HttpResponse(self.get_success_url())

# class MovieDescriptionView(SuccessMessageMixin, UpdateView):
#     """Movies that are now in the cinema. url: 'movies/'. TODO"""
#     template_name = 'admin_lte/pages/movie_description.html'
#     model = Movie
#     form_class = MovieForm
#     form_class2 = SeoDataForm
#     success_message = 'Success'
#     success_url = reverse_lazy('movies_list')
#
#     def get_context_data(self, **kwargs):
#         context = super(MovieDescriptionView, self).get_context_data(**kwargs)
#         context['form2'] = self.form_class2(instance=self.object.seo)
#         return context
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#
#         if not request.user.is_authenticated:
#             return HttpResponseForbidden
#
#         form1 = MovieForm(request.POST)
#         form2 = SeoDataForm(request.POST)
#
#         f1_valid = form1.is_valid()
#         f2_valid = form2.is_valid()
#         if f1_valid or f2_valid:
#             print('go')
#             form2.save()
#             # form2.save()
#             # form2.save()
#             # new_form = Movie()
#             # newdoc.save()
#
#             # Redirect to the document list after POST
#         return reverse('movies_list')
#
#         # if form.is_valid():
#         #     return self.form_valid(form)
#         # else:
#         #     return self.form_invalid(form)
#
#     def form_valid(self, form):
#         current_task = get_object_or_404(Movie, slug=self.kwargs['slug'])
#         self.object = form.save(commit=False)
#         self.object.task = current_task
#         self.object.save()
#         return HttpResponse(self.get_success_url())
# ---------------def form_valid(self, form):
#     current_task = get_object_or_404(Task, slug=self.kwargs['slug'])
#     self.object = form.save(commit=False)
#     self.object.task =  current_task
#     self.object.save()
#     return HttpResponse(self.get_success_url())

# def get_update_url(self):
#     return reverse('quiz_update', kwargs={'slug': self.url})

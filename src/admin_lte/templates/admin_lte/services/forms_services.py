from django.utils.datetime_safe import date
from admin_lte.forms import ImageForm, SeoDataForm, ArticleForm
from cinema_site.models import Image, Article, Gallery, SeoData
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404


def get_article_qs(mode):
    return Article.objects.filter(mode=mode)


def save_new_images_to_gallery(obj, request):
    undefined_images = request.FILES.getlist('formset-undefined-image')
    if undefined_images:
        images = []

        for image in undefined_images:
            gallery_image = Image(image=image, gallery=obj.gallery)
            images.append(gallery_image)

        Image.objects.bulk_create(images)


def append_forms_validation(iterable_obj, validation_list):
    for form in iterable_obj:
        if form.is_valid():
            validation_list.append(True)
        else:
            validation_list.append(False)


def validate_forms(*args, formset=None):
    validation_list = []
    if args:
        append_forms_validation(args, validation_list)

    if formset:
        validation_list.append(formset.is_valid())
        append_forms_validation(formset, validation_list)

    if all(validation_list):
        return True
    else:
        return False


def save_objects(*args):
    for obj in args:
        obj.save()


def save_forms(*args):
    for form in args:
        form.save(commit=True)


def get_url_path(self):
    return self.request.META.get('PATH_INFO', None)


def create_forms(obj, obj_form, gallery, request):
    formset_factory = modelformset_factory(Image, form=ImageForm, fields={'image', }, extra=0)
    obj_form_inst = obj_form(request.POST or None, request.FILES or None, prefix='form1', instance=obj)
    seo_data_form = SeoDataForm(request.POST or None, prefix='form2', instance=obj.seo)
    formset = formset_factory(request.POST or None, request.FILES or None, prefix='formset', queryset=gallery)
    return obj_form_inst, seo_data_form, formset


def get_objects(obj_class, slug, qs=None, trailer=True):
    if qs:
        obj = qs.get(slug=slug)
    else:
        obj = get_object_or_404(obj_class, slug=slug)
        print(obj)

    gallery = Image.objects.filter(gallery=obj.gallery)

    if trailer:
        video_url = obj.trailer_url.split('=')[1]
        return obj, gallery, video_url
    else:
        return obj, gallery


def create_objects(mode):
    gallery_inst = Gallery()
    seo_inst = SeoData()
    article = Article(is_active=True, publication=date.today(), mode=mode, gallery=gallery_inst, seo=seo_inst)
    gallery_images = Image.objects.filter(gallery=gallery_inst)
    return article, gallery_images, gallery_inst, seo_inst

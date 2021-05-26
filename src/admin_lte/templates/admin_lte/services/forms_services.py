from admin_lte.forms import ImageForm, SeoDataForm
from cinema_site.models import Image, Article
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404


news_qs = Article.objects.filter(mode='NEWS')
events_qs = Article.objects.filter(mode='NEWS')


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


def save_forms(*args):
    for form in args:
        form.save(commit=True)


def create_forms(obj, obj_form, gallery, request):
    formset_factory = modelformset_factory(Image, form=ImageForm, fields={'image', }, extra=0, max_num=6)
    formset = formset_factory(request.POST or None, request.FILES or None, prefix='formset', queryset=gallery)
    obj_form_inst = obj_form(request.POST or None, request.FILES or None, prefix='form1', instance=obj)
    seo_data_form = SeoDataForm(request.POST, prefix='form2', instance=obj.seo)
    return obj_form_inst, seo_data_form, formset


def get_objects(obj_class, slug, qs=None, trailer=True):
    if qs:
        obj = qs.get(slug=slug)
    else:
        obj = get_object_or_404(obj_class, slug=slug)

    gallery = Image.objects.filter(gallery=obj.gallery)

    if trailer:
        video_url = obj.trailer_url.split('=')[1]
        return obj, gallery, video_url
    else:
        return obj, gallery

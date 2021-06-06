from django.shortcuts import get_object_or_404
from cinema_site.models import Page, Image


def fill_context_for_standard_page_1(context, page_title):
    page = get_object_or_404(Page, title=page_title)
    images = Image.objects.filter(gallery=page.gallery)
    context.update({
        'page': page,
        'images': images,
    })

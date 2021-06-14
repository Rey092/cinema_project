from django.shortcuts import get_object_or_404
from cinema_site.models import Page, Image


def fill_context_for_standard_page_1(context, page_title):
    page = Page.objects.get_or_create(title=page_title)[0]
    images = Image.objects.filter(gallery=page.gallery)
    context.update({
        'page': page,
        'images': images,
    })

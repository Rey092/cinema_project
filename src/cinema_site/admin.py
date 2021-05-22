"""Register your models here."""
from django.contrib import admin

from .models import Article, Cinema, Contacts, EmailTemplate, Hall, Image, Movie, MovieGalleryImage, Page, \
    Seance, SeoData, Ticket

admin.site.register(Image)
admin.site.register(SeoData)
admin.site.register(Cinema)
admin.site.register(Hall)
admin.site.register(MovieGalleryImage)
admin.site.register(Movie)
admin.site.register(Seance)
admin.site.register(Ticket)
admin.site.register(Article)
admin.site.register(Page)
admin.site.register(Contacts)
admin.site.register(EmailTemplate)

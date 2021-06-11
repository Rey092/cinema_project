"""Register your models here."""
from django.contrib import admin

from .models import Article, Cinema, Contacts, EmailTemplate, Gallery, Hall, Image, Movie, Page, \
    Seance, SeoData, Ticket, Logger

admin.site.register(SeoData)
admin.site.register(Cinema)
admin.site.register(Hall)
admin.site.register(Movie)
admin.site.register(Seance)
admin.site.register(Ticket)
admin.site.register(Article)
admin.site.register(Page)
admin.site.register(Contacts)
admin.site.register(EmailTemplate)
admin.site.register(Image)
admin.site.register(Gallery)
admin.site.register(Logger)

"""Register your models here."""
from django.contrib import admin

from .models import News, Cinema, Contacts, EmailTemplate, Gallery, Hall, Image, Movie, Page, \
    Seance, SeoData, Ticket

admin.site.register(SeoData)
admin.site.register(Cinema)
admin.site.register(Hall)
admin.site.register(Movie)
admin.site.register(Seance)
admin.site.register(Ticket)
admin.site.register(News)
admin.site.register(Page)
admin.site.register(Contacts)
admin.site.register(EmailTemplate)
admin.site.register(Image)
admin.site.register(Gallery)

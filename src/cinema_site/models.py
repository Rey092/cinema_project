import os

from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from profiles.models import UserProfile

from .services.media_services import UploadToPathAndRename


class Gallery(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.name) or ''


class Image(models.Model):
    image = models.ImageField(upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'images')))
    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, null=True)

    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return str(self.text) or ''


class SeoData(models.Model):
    title = models.CharField(max_length=40)
    url = models.URLField()
    keywords = models.CharField(max_length=200)
    description = models.TextField()
    seo_text = models.TextField()


class Cinema(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    conditions = models.TextField()

    logo = models.ImageField(
        upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'images', 'cinemas', str(name), 'logos')))
    banner = models.ImageField(
        upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'images', 'cinemas', str(name), 'banners')))

    seo = models.ForeignKey(SeoData, on_delete=models.SET_NULL, null=True)
    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, null=True)


class Hall(models.Model):
    class Meta:
        unique_together = [('hall_number', 'cinema')]

    hall_number = models.CharField(max_length=2)
    description = models.TextField()
    conditions = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    layout = models.ImageField(upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'halls', 'layouts')))
    banner = models.ImageField(upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'halls', 'banners')))

    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, null=True)
    seo = models.ForeignKey(SeoData, on_delete=models.SET_NULL, null=True, related_name='hall_seo')
    cinema = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True, related_name='hall_cinema')


class Movie(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40, unique=True)
    description = models.TextField()
    trailer_url = models.URLField()
    release_date = models.DateField()
    is_active = models.BooleanField()
    is_2d = models.BooleanField()
    is_3d = models.BooleanField()
    is_imax = models.BooleanField()

    poster = models.ImageField(upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'movies', 'posters')))

    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, null=True)
    seo = models.ForeignKey(SeoData, on_delete=models.SET_NULL, null=True, related_name='movie_seo')

    def __str__(self):
        return self.title


class Seance(models.Model):
    class Format(models.TextChoices):
        FORMAT_3D = '3D', _('3D')
        FORMAT_2D = '2D', _('2D')
        FORMAT_IMAX = 'IMAX', _('IMAX')

    seance_format = models.CharField(max_length=4, choices=Format.choices, verbose_name='Формат фильма')
    price = models.IntegerField()
    time = models.DateTimeField()

    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True, related_name='seance_movie')
    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True, related_name='seance_hall')


class Ticket(models.Model):
    class Meta:
        unique_together = [('row', 'seat_place', 'seance')]

    row = models.IntegerField()
    seat_place = models.IntegerField()
    is_paid = models.BooleanField(default=False)

    seance = models.ForeignKey(Seance, on_delete=models.SET_NULL, null=True, related_name='ticket_seance')
    buyer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='ticket_buyer')


class Article(models.Model):

    class Mode(models.TextChoices):
        NEWS = 'NEWS', _('Новость')
        EVENTS = 'EVENTS', _('Акция')

    title = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    trailer_url = models.URLField()
    is_active = models.BooleanField()
    publication = models.DateField(db_index=True)

    mode = models.CharField(max_length=6, choices=Mode.choices, verbose_name='Тип')

    banner = models.ImageField(upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'articles', 'banners')))

    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, null=True)
    seo = models.ForeignKey(SeoData, on_delete=models.SET_NULL, null=True, related_name='article_seo')

    def __str__(self):
        return self.title


class Page(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    phone1 = PhoneNumberField(null=True, blank=True)
    phone2 = PhoneNumberField(null=True, blank=True)
    is_basic = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)

    banner = models.ImageField(upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'pages', 'banners')))

    gallery = models.ForeignKey(Gallery, on_delete=models.SET_NULL, null=True)
    seo = models.ForeignKey(SeoData, on_delete=models.SET_NULL, null=True, related_name='page_seo')

    def __str__(self):
        return self.title


class Contacts(models.Model):
    name = models.CharField(max_length=40)
    address = models.TextField()
    coordinates = models.TextField(max_length=800)
    is_active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)

    logo = models.ImageField(upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'contacts', 'logos')))
    banner = models.ImageField(upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'contacts', 'banner')))

    def __str__(self):
        return self.name


class EmailTemplate(models.Model):
    file = models.FileField()
    created = models.DateTimeField(auto_now_add=True)

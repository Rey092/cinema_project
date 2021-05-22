import os

from django.conf.global_settings import MEDIA_ROOT
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from profiles.models import UserProfile

from .services.media_services import UploadToPathAndRename


class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'images')))

    def __str__(self):
        return self.name


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

    logo = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name='cinema_logo')
    banner = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name='cinema_banner')
    seo = models.ForeignKey(SeoData, on_delete=models.SET_NULL, null=True, related_name='cinema_seo')


class Hall(models.Model):
    hall_number = models.CharField(max_length=2)
    slug = models.SlugField()
    description = models.TextField()
    conditions = models.TextField()

    cinema = models.ForeignKey(Cinema, on_delete=models.SET_NULL, null=True, related_name='hall_cinema')
    layout = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name='hall_layout')
    banner = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name='hall_banner')
    seo = models.ForeignKey(SeoData, on_delete=models.SET_NULL, null=True, related_name='hall_seo')


class Movie(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40)
    description = models.TextField()
    trailer_url = models.URLField()
    release_date = models.DateField()
    is_active = models.BooleanField()
    is_2d = models.BooleanField()
    is_3d = models.BooleanField()
    is_imax = models.BooleanField()

    poster = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name='movie_poster')
    seo = models.ForeignKey(SeoData, on_delete=models.SET_NULL, null=True, related_name='movie_seo')


class MovieGalleryImage(models.Model):
    image = models.ImageField(upload_to=UploadToPathAndRename(os.path.join(MEDIA_ROOT, 'images')))
    movie = models.ForeignKey(Movie, on_delete=models.SET_NULL, null=True)


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
    row = models.IntegerField()
    seat_place = models.IntegerField()
    is_booked = models.BooleanField()

    seance = models.ForeignKey(Seance, on_delete=models.SET_NULL, null=True, related_name='ticket_seance')
    buyer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, related_name='ticket_buyer')


class Article(models.Model):
    class Mode(models.TextChoices):
        NEWS = 'NEWS', _('Новость')
        EVENT = 'EVENT', _('Акция')
    title = models.CharField(max_length=40)
    slug = models.SlugField()
    description = models.TextField()
    video_url = models.URLField()
    is_active = models.BooleanField()
    mode = models.CharField(max_length=5, choices=Mode.choices, null=True, verbose_name='Тип статьи')
    created = models.DateTimeField(auto_now_add=True)

    banner = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name='article_banner')
    seo = models.ForeignKey(SeoData, on_delete=models.SET_NULL, null=True, related_name='article_seo')


class Page(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField()
    description = models.TextField()
    phone1 = PhoneNumberField()
    phone2 = PhoneNumberField()
    is_basic = models.BooleanField(default=True)

    banner = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name='page_banner')
    seo = models.ForeignKey(SeoData, on_delete=models.SET_NULL, null=True, related_name='page_seo')


class Contacts(models.Model):
    name = models.CharField(max_length=40)
    address = models.TextField()
    coordinates = models.CharField(max_length=120)

    logo = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, related_name='contacts_logo')


class EmailTemplate(models.Model):
    file = models.FileField()
    created = models.DateTimeField(auto_now_add=True)

from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from profiles.models import UserProfile


class Image(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='media/admin_lte/')


class SeoData(models.Model):
    title = models.CharField(max_length=40)
    url = models.URLField()
    keywords = models.CharField(max_length=200)
    description = models.TextField()
    seo_text = models.TextField()


class Cinema(models.Model):
    name = models.CharField(max_length=40)
    slug = models.SlugField()
    description = models.TextField()
    conditions = models.TextField()

    logo = models.ForeignKey(Image, on_delete=models.CASCADE)
    banner = models.ForeignKey(Image, on_delete=models.CASCADE)
    seo = models.ForeignKey(SeoData, on_delete=models.CASCADE)


class Hall(models.Model):
    hall_number = models.CharField(max_length=2)
    slug = models.SlugField()
    description = models.TextField()
    conditions = models.TextField()

    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
    layout = models.ForeignKey(Image, on_delete=models.CASCADE)
    banner = models.ForeignKey(Image, on_delete=models.CASCADE)
    seo = models.ForeignKey(SeoData, on_delete=models.CASCADE)


class Movie(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField(max_length=40)
    description = models.TextField()
    trailer_url = models.URLField()
    release_date = models.DateField()
    is_active = models.BooleanField()

    poster = models.ForeignKey(SeoData, on_delete=models.CASCADE)
    seo = models.ForeignKey(SeoData, on_delete=models.CASCADE)


class Seance(models.Model):
    class Format(models.TextChoices):
        FORMAT_3D = '3D', _('3D')
        FORMAT_2D = '2D', _('2D')
        FORMAT_IMAX = 'IMAX', _('IMAX')

    seance_format = models.CharField(max_length=4, choices=Format.choices, verbose_name='Формат фильма')
    price = models.IntegerField()
    time = models.DateTimeField()

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE)


class Ticket(models.Model):
    row = models.IntegerField()
    seat_place = models.IntegerField()
    is_booked = models.BooleanField()

    seance = models.ForeignKey(Seance, on_delete=models.CASCADE)
    buyer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Article(models.Model):
    class Mode(models.TextChoices):
        NEWS = 'NEWS', _('Новость')
        EVENT = 'EVENT', _('Акция')
    title = models.CharField(max_length=40)
    slug = models.SlugField()
    description = models.TextField()
    video_url = models.URLField()
    is_active = models.BooleanField()
    mode = models.CharField(max_length=5, choices=Mode.choices, verbose_name='Тип статьи')
    created = models.DateTimeField(auto_now_add=True)

    banner = models.ForeignKey(Image, on_delete=models.CASCADE)
    seo = models.ForeignKey(SeoData, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Page(models.Model):
    title = models.CharField(max_length=40)
    slug = models.SlugField()
    description = models.TextField()
    phone1 = PhoneNumberField()
    phone2 = PhoneNumberField()
    is_basic = models.BooleanField(default=True)

    banner = models.ForeignKey(Image, on_delete=models.CASCADE)
    seo = models.ForeignKey(SeoData, on_delete=models.CASCADE)


class Contacts(models.Model):
    name = models.CharField(max_length=40)
    address = models.TextField()
    coordinates = models.CharField(max_length=120)
    logo = models.ForeignKey(Image, on_delete=models.CASCADE)


class EmailTemplate(models.Model):
    file = models.FileField()
    created = models.DateTimeField(auto_now_add=True)

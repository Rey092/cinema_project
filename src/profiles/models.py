from creditcards.models import CardNumberField
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import DateField
from django.utils.translation import gettext_lazy as _
from phonenumber_field import modelfields


def normalize_all(obj):
    obj.email = UserProfileManager.normalize_email(obj.email)
    obj.username = UserProfile.normalize_username(obj.username)

    obj.username = obj.username.lower()
    obj.email = obj.email.lower()
    obj.first_name = obj.first_name.capitalize()
    obj.last_name = obj.last_name.capitalize()
    obj.full_name = f'{obj.first_name} {obj.last_name}'


class UserProfileManager(BaseUserManager):
    """Manager for user profiles."""

    def create_user(self, email, username, password=None, *args, **kwargs):
        """Create a new user profile."""
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')

        user = self.model(email, username, *args, **kwargs)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, *args, **kwargs):
        """Create and save a new superuser with given details."""
        user = self.create_user(*args, **kwargs)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system."""

    class Languages(models.TextChoices):
        ENGLISH = 'EN', _('Английский')
        RUSSIAN = 'RU', _('Русский')

    class Genders(models.TextChoices):
        MALE = 'M', _('Мужчина')
        FEMALE = 'F', _('Женщина')

    class Cities(models.TextChoices):
        ODESSA = 'ODESSA', _('Одесса')
        KIEV = 'KIEV', _('Киев')
        KHARKIV = 'KHARKIV', _('Харьков')

    username = models.CharField(max_length=20, unique=True, verbose_name='Никнейм')
    email = models.EmailField(max_length=100, unique=True, verbose_name='Электронная почта')
    first_name = models.CharField(max_length=20, verbose_name='Имя')
    last_name = models.CharField(max_length=20, verbose_name='Фамилия')
    full_name = models.CharField(max_length=40, verbose_name='Полное имя')
    phone_number = modelfields.PhoneNumberField(verbose_name='Номер телефона')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    cc_number = CardNumberField(_('Номер карты'))
    birthday = DateField(verbose_name='Дата рождения')
    created = DateField(auto_now_add=True)

    language = models.CharField(max_length=2, choices=Languages.choices, default=Languages.RUSSIAN, verbose_name='Язык')
    gender = models.CharField(max_length=1, choices=Genders.choices, default=Genders.MALE, verbose_name='Пол')
    city = models.CharField(max_length=20, choices=Cities.choices, default=Cities.ODESSA, verbose_name='Город')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number', 'address', 'birthday', 'gender', 'city']

    def get_language(self):
        return self.language

    def get_full_name(self):
        """Retrieve full name of user."""
        return self.full_name

    def get_first_name(self):
        """Retrieve short name of user."""
        return self.first_name

    def get_last_name(self):
        """Retrieve short name of user."""
        return self.last_name

    def __str__(self):
        """Return string representation of our user."""
        return self.email

    def save(self, *args, **kwargs):
        normalize_all(self)
        super(UserProfile, self).save(*args, **kwargs)

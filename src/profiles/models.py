from creditcards.models import CardNumberField
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import DateField
from django.utils.translation import gettext_lazy as _
from phonenumber_field import modelfields


class UserProfileManager(BaseUserManager):
    """Manager for user profiles."""

    def create_user(self, email, password=None, *args, **kwargs):
        """Create a new user profile."""
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email, *args, **kwargs)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, *args, **kwargs):
        """Create and save a new superuser with given details."""
        user = self.create_user(email, *args, **kwargs)

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

    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    full_name = models.CharField(max_length=40)
    phone_number = modelfields.PhoneNumberField()
    address = models.CharField(max_length=40)
    cc_number = CardNumberField(_('card number'))
    birthday = DateField()
    created = DateField(auto_now_add=True)

    language = models.CharField(max_length=2, choices=Languages.choices, default=Languages.RUSSIAN,)
    gender = models.CharField(max_length=1, choices=Genders.choices, default=Genders.MALE,)
    city = models.CharField(max_length=20, choices=Cities.choices, default=Cities.ODESSA,)

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
        self.full_name = f'{self.first_name} {self.last_name}'
        super(UserProfile, self).save(*args, **kwargs)

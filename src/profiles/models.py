from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserProfileManager(BaseUserManager):
    """Manager for user profiles."""

    def create_user(self, email, first_name, last_name, password=None):
        """Create a new user profile."""
        if not email:
            raise ValueError('User must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password):
        """Create and save a new superuser with given details."""
        user = self.create_user(email, first_name, last_name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system."""

    email = models.EmailField(max_length=100, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    full_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

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

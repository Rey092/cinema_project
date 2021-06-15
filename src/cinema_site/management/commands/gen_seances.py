import random

from django.core.management import BaseCommand
from django.db import IntegrityError
from django.utils.datetime_safe import datetime
from django.utils.timezone import get_current_timezone
from faker import Faker
from cinema_site.models import Seance, Movie, Hall


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(400):
            try:
                Seance(
                    seance_format=random.choice(['3D', '2D', 'IMAX']),
                    price=random.randint(100, 200),
                    time=fake.date_time_between(start_date='now', end_date='+50d', tzinfo=get_current_timezone()),
                    movie=random.choice(
                        list(Movie.objects.filter(is_active=True, release_date__lte=datetime.today()))),
                    hall=random.choice(list(Hall.objects.all()))
                ).save()
            except IntegrityError:
                pass

import random

from django.core.management import BaseCommand
from django.db import IntegrityError
from faker import Faker
from profiles.models import UserProfile


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker()
        for _ in range(45):
            try:
                UserProfile(
                    username=fake.language_name(),
                    email=fake.email(),
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    phone_number=f'{fake.country_calling_code()}'.replace(' ', '') + str(
                        fake.random_number(digits=9, fix_len=True)),
                    address=fake.address(),
                    cc_number=fake.credit_card_number(),
                    birthday=fake.date(),
                    language=random.choice(['EN', 'RU']),
                    gender=random.choice(['F', 'M']),
                    city=random.choice(['ODESSA', 'KIEV', 'KHARKIV'])
                ).save()
            except IntegrityError:
                pass

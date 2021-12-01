from django.core.management import BaseCommand
from core.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users = User.objects.using('old').all()
        for user in users:
            print(f'populate user -> first_name:{user.first_name} last_name:{user.last_name}')
            user = User.objects.create(
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                password=user.password,
                is_ambassador=user.is_ambassador
            )
            user.set_password('1234')
            user.save()

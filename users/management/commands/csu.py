from django.core.management import BaseCommand
import os
from users.models import User
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

dot_env = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=dot_env)


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email="a@a.a",
            first_name="Mer1d1an",
            last_name="Nikita",
            is_staff=True,
            is_superuser=True,
            is_active=True,
        )
        user.set_password(os.getenv("EMAIL_PASS"))
        user.save()

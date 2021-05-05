"""Customized createsuper user command that won't crush the app
if the user already exists
"""
# Builtins
from typing import Any, Optional

# Third party
from decouple import config
# Django
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create default admin if none exists"""

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        if get_user_model().objects.count() == 0:
            email = config("DJANGO_SUPERUSER_EMAIL")
            password = config("DJANGO_SUPERUSER_PASSWORD")
            username = config("DJANGO_SUPERUSER_USERNAME")
            default_admin = get_user_model().objects.create_superuser(
                email=email, username=username, password=password
            )
            default_admin.is_active = True
            default_admin.is_admin = True
            default_admin.save()
            self.stdout.write(
                self.style.SUCCESS("Default admin successfully created!")
            )
            return default_admin.username
        self.stdout.write(self.style.ERROR("Default admin already exists."))
        return ""

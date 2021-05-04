"""Wait for db command for docker so that it doesn't crash
"""
# Builtins
import time

# Django
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to pause execution until database is available"""

    def handle(self, *args, **kwargs):
        self.stdout.write("Waiting for database ...")
        db_conn = None
        while db_conn is None:
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))

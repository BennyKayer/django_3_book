"""Register models for django admin panel
"""
# Django
from django.contrib import admin
from core.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "date_of_birth", "photo"]

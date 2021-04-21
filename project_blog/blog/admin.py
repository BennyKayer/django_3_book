from django.contrib import admin

from .models import Comment, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Customize model display in admin panel
    list_display: controls which columns are dispalyed in all rows view
    list_filter: adds right panel with filtering capabilities
    search_fields: adds search bar up top that searches by fields specified
    date_hierachy: underneatch search field for date hierarchy searching
    prepopulated_fields: fills slug with title while typing in post creation
    raw_id_fields: advanced widget instead of drop-down
    ordering: controls default ordering
    """

    list_display = ("title", "author", "publish", "status")
    list_filter = ("status", "created", "publish", "author")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    raw_id_fields = ("author",)
    date_hierarchy = "publish"
    ordering = ("status", "publish")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Custom model display in admin panel"""

    list_display = (
        "name",
        "email",
        "post",
        "created",
        "active",
    )
    list_filter = (
        "active",
        "created",
        "updated",
    )
    search_fields = (
        "name",
        "email",
        "body",
    )

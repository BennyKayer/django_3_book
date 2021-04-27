"""
1. Nazwa pliku jest ważna ponieważ będzie wykorzystana do wczytania znaczników w szablonach.
2. 1wszy rodzaj tagów simple_tag => Przetworzenie danych i zwrot ciągu tekstowego
3. 2gi rodzaj tagów inclusion_tag => Przetworzenie danych i zwrot wygenerowanego szablonu
"""
from django import template
from blog.models import Post
from django.db.models import Count

# musi być register żeby było uznawane za znacznik
register = template.Library()


# można pominąć nawiasy przy simple tag, domyślnie i tak będzie taka nazwa
@register.simple_tag(name="total_posts")
def total_posts():
    """Return total number of posts published"""
    return Post.published.count()


@register.inclusion_tag("blog/post/latest_posts.html")
def show_latest_posts(count: int = 5):
    """Wygeneruj nieuporządkowaną listę najnowszych postów

    Args:
        count (int, optional): Liczba najnowszych postów. Defaults to 5.

    Returns:
        latest_posts.html: Szablon z dostępem do zmiennej z daną liczbą ostatnich postów
    """

    latest_posts = Post.published.order_by("-publish")[:count]
    return {"latest_posts": latest_posts}


@register.simple_tag
def get_most_commented_posts(count: int = 5):
    return Post.published.annotate(total_comments=Count("comments")).order_by(
        "-total_comments"
    )[:count]

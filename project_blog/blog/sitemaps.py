"""Sitemap'y to pliki XML przekazujące wyszukiwarkom informacje o stronach w witrynie
łatwiej im wtedy to indexować
"""
from django.contrib.sitemaps import Sitemap
from blog.models import Post


class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Post.published.all()

    def lastmod(self, obj):
        return obj.publish

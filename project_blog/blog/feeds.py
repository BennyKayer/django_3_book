from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from blog.models import Post


class LatestPostsFeed(Feed):
    title = "Mój blog"
    # <link> RSS
    link = "/blog/"
    description = "Nowe posty na moim blogu"

    def items(self):
        return Post.published.all()[:5]

    # <title> RSS
    def item_title(self, item: Post):
        return item.title

    # <description> kanału RSS
    def item_description(self, item: Post) -> str:
        return truncatewords(item.body, 30)

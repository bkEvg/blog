from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Post


class StaticViewSitemap(Sitemap):
    """Static view settings for SEO opt.

    Args:
        Sitemap (_type_): base class
    """
    priority = 0.99
    changefreq = 'weekly'

    def items(self):
        return ['post_list']

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
    """Post list sitemap settings for SEO opt.

    Args:
        Sitemap (_type_): base class
    """
    changefreq = 'daily'
    priority = 0.9

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.publish

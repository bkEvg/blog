from django.contrib.sitemaps import Sitemap
from .models import Post
from django.urls import reverse


class StaticViewSitemap(Sitemap):
    priority = 0.99
    changefreq = 'weekly'

    def items(self):
        return ['post_list']

    def location(self, item):
        return reverse(item)


class PostSitemap(Sitemap):
	changefreq = 'daily'
	priority = 0.9

	def items(self):
		return Post.objects.filter(status='published')

	def lastmod(self, obj):
		return obj.publish
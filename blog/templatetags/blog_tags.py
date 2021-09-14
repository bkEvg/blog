from django import template
from django.db.models import Count
from taggit.models import Tag


register = template.Library()

from ..models import Post

@register.simple_tag
def total_posts():
	return Post.objects.filter(status='published').count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
	latest_posts = Post.objects.filter(status='published').order_by('-publish')[:count]
	return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
	return Post.objects.filter(status='published').annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
	
@register.simple_tag
def get_most_popular_posts(count=5):
	return Post.objects.filter(status='published').annotate(total_views=Count('views')).order_by('-total_views')[:count]

@register.simple_tag
def get_most_popular_tags(count=8):
	return Tag.objects.all().filter(slug__isnull=False).annotate(total_posts=Count('posts')).order_by('-total_posts')[:count]
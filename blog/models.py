from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.shortcuts import get_object_or_404
from django.db.models import Count


class Author(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	profile_image = models.ImageField(upload_to='media/profile_images', default='default.jpeg', verbose_name='Фото профиля')
	first_name = models.CharField(max_length=200, blank=True, verbose_name='Имя')
	last_name = models.CharField(max_length=200, blank=True, verbose_name='Фамилия')

	class Meta:
		verbose_name = 'автор'
		verbose_name_plural = 'авторы'
			

	def __str__(self):
		return self.user.username

	def get_full_name(self):
		return f'{self.first_name} {self.last_name}'


class Post(models.Model):
	STATUS_CHOICES = (
		('draft', 'Черновик'),
		('published', 'Готов'),
	)
	cover = models.ImageField(upload_to='media/blog_covers/%d.%m.%Y/', default='default_cover.jpeg', verbose_name='Обложка')
	title = models.CharField(max_length=250, verbose_name='Заголовок')
	slug = models.SlugField(max_length=250, unique_for_date='publish')
	author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Автор')
	body = RichTextField(blank=True)
	publish = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
	tags = TaggableManager(verbose_name='Тэги', related_name='posts')

	class Meta:
		ordering = ('-publish',)
		verbose_name = 'пост'
		verbose_name_plural = 'посты'

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post_detail', args=[self.publish.year, self.slug])

		# return reverse('post_detail', args=[self.publish.strftime('%d'), self.slug])

	def get_previous_post(self):
		post = get_object_or_404(Post, slug=self.slug, status='published', publish=self.publish)
		post_tags_ids = post.tags.values_list('id', flat=True)
		similar_posts = Post.objects.filter(tags__in=post_tags_ids, status='published', created__lt=self.created).exclude(id=post.id)
		similar_post = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')
		if similar_post:
			return similar_post
		else:
			post_=Post.objects.filter(status='published', created__lt=self.created)
			if post_:
				return post_
			else:
				pass

	def get_next_post(self):
		post = get_object_or_404(Post, slug=self.slug, status='published', publish=self.publish)
		post_tags_ids = post.tags.values_list('id', flat=True)
		similar_posts = Post.objects.filter(tags__in=post_tags_ids, status='published', created__gt=self.created).exclude(id=post.id)
		similar_post = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')
		if similar_post:
			return similar_post
		else:
			post_=Post.objects.filter(status='published', created__gt=self.created)
			if post_:
				return post_
			else:
				pass

class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	name = models.CharField(max_length=80)
	email = models.EmailField()
	body = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)

	class Meta:
		ordering = ('created',)
		verbose_name = 'комментарий'
		verbose_name_plural = 'комментарии'

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)


class UniqueView(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
	ip = models.GenericIPAddressField()

	class Meta:
		verbose_name = 'просмотр'
		verbose_name_plural = 'просмотры'

	def __str__(self):
		return self.ip

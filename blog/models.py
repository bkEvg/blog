from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from django.shortcuts import get_object_or_404
from django.db.models import Count

# from django.utils.text import slugify


class TagBase(models.Model):
    name = models.CharField(verbose_name="name", unique=True, max_length=100)
    slug = models.SlugField(verbose_name="slug", unique=True, max_length=100)

    def __str__(self):
        return self.name

    def __gt__(self, other):
        return self.name.lower() > other.name.lower()

    def __lt__(self, other):
        return self.name.lower() < other.name.lower()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self._state.adding and not self.slug:
            self.slug = self.slugify(self.name)
            using = kwargs.get("using") or router.db_for_write(
                type(self), instance=self
            )
            # Make sure we write to the same db for all attempted writes,
            # with a multi-master setup, theoretically we could try to
            # write and rollback on different DBs
            kwargs["using"] = using
            # Be opportunistic and try to save the tag, this should work for
            # most cases ;)
            try:
                with transaction.atomic(using=using):
                    res = super().save(*args, **kwargs)
                return res
            except IntegrityError:
                pass
            # Now try to find existing slugs with similar names
            slugs = set(
                type(self)
                ._default_manager.filter(slug__startswith=self.slug)
                .values_list("slug", flat=True)
            )
            i = 1
            while True:
                slug = self.slugify(self.name, i)
                if slug not in slugs:
                    self.slug = slug
                    # We purposely ignore concurrency issues here for now.
                    # (That is, till we found a nice solution...)
                    return super().save(*args, **kwargs)
                i += 1
        else:
            return super().save(*args, **kwargs)

    def slugify(self, tag, i=None):
        slug = slugify(tag)
        if i is not None:
            slug += "_%d" % i
        return slug


class Author(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
	profile_image = models.ImageField(upload_to='profile_images', default='default.jpeg', verbose_name='Фото профиля')
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
	cover = models.ImageField(upload_to='blog_covers/%d.%m.%Y/', default='default_cover.jpeg', verbose_name='Обложка')
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
		return reverse('post_detail', args=[self.publish.strftime('%d'),
										self.publish.strftime('%m'),
										self.publish.strftime('%Y'),
										self.slug])

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

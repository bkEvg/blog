from django.contrib.auth.models import User
from django.db import models
from django.db.models import Count
from django.utils import timezone
from django.urls import reverse

from taggit.managers import TaggableManager
from ckeditor_uploader.fields import RichTextUploadingField


class Author(models.Model):
    """Author model

    Args:
        models (_type_): base class
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    profile_image = models.ImageField(upload_to='media/profile_images', 
                                      default='default.jpeg',
                                      verbose_name='Фото профиля')
    first_name = models.CharField(max_length=200, blank=True,
                                  verbose_name='Имя')
    last_name = models.CharField(max_length=200, blank=True,
                                 verbose_name='Фамилия')

    class Meta:
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        if not self.first_name or not self.last_name:
            return self.user.username
        else:
            return f'{self.first_name} {self.last_name}'


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Готов'),
    )
    cover = models.ImageField(upload_to='media/blog_covers/%d.%m.%Y/',
                              default='default_cover.jpeg',
                              verbose_name='Обложка')
    title = models.CharField(max_length=250, verbose_name='Заголовок')
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ForeignKey(Author, on_delete=models.CASCADE,
                               related_name='blog_posts',
                               verbose_name='Автор')
    description = models.CharField(default='None', max_length=250,
                                   verbose_name="Описание для продвижения")
    body = RichTextUploadingField(blank=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='draft', verbose_name='Статус')
    tags = TaggableManager(verbose_name='Тэги', related_name='posts')

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'пост'
        verbose_name_plural = 'посты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])

    def get_previous_post(self):
        post_tags_ids = self.tags.values_list('id', flat=True)
        similar_posts = (Post.objects.
                         filter(tags__in=post_tags_ids, status='published',
                                created__lt=self.creat).exclude(id=self.id)
                         .annotate(same_tags=Count('tags'))
                         .order_by('-same_tags', '-publish'))

        if not similar_posts.exists():
            similar_posts = Post.objects.filter(
                status='published',
                created__lt=self.created
            ).exclude(id=self.id).order_by('-publish')
        return similar_posts.first()

    def get_next_post(self):
        post_tags_ids = self.tags.values_list('id', flat=True)
        similar_posts = (Post.objects
                         .filter(tags__in=post_tags_ids,
                                 status='published',
                                 created__gt=self.created)
                         .exclude(id=self.id)
                         .annotate(same_tags=Count('tags'))
                         .order_by('-same_tags', '-publish'))
        if not similar_posts.exists():
            similar_posts = Post.objects.filter(
                status='published',
                created__gt=self.created
            ).exclude(id=self.id).order_by('-publish')
        return similar_posts.first()


class Comment(models.Model):
    """Comment model

    Args:
        models (_type_): base class
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
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
        return 'Комментарий от {} на {}'.format(self.name, self.post.title)


class UniqueView(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='views')
    ip = models.GenericIPAddressField()

    class Meta:
        verbose_name = 'просмотр'
        verbose_name_plural = 'просмотры'

    def __str__(self):
        return f"Просмотр от {self.ip} на {self.post.title}"

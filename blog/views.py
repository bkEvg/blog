from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Count
from django.db.models import F
from .helpers import get_client_ip
from .models import UniqueView, Comment
from django.db.models import Count
from django.contrib import messages
from django.db.models import Count



def list(request, tag_slug=None):
	object_list = Post.objects.filter(status='published').order_by('-created')

	tag = None
	# tags = Tag.objects.all().filter(slug__isnull=False).annotate(total_posts=Count('posts')).order_by('-total_posts')

	if tag_slug:
	    tag = get_object_or_404(Tag, slug=tag_slug)
	    object_list = object_list.filter(tags__in=[tag])

	paginator = Paginator(object_list, 10)  # posts in each page
	page = request.GET.get('page')
	try:
	    posts = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer deliver the first page
	    posts = paginator.page(1)
	except EmptyPage:
	    # If page is out of range deliver last page of results
	    posts = paginator.page(paginator.num_pages)
	return render(request,
	              'blog/post/list.html',
	              {'page': page,
	               'posts': posts,
	               'tag': tag})



def detail(request, year, post):

	post = get_object_or_404(Post, slug=post, status='published', publish__year=year)
	post_tags_ids = post.tags.values_list('id', flat=True)
	similar_posts = Post.objects.filter(tags__in=post_tags_ids, status='published').exclude(id=post.id)
	similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
	comments = Comment.objects.filter(post=post, active=True).order_by('-created')
	views = UniqueView.objects.filter(post=post)
	# List of active comments for this post
	comments = post.comments.filter(active=True)

	if request.method == 'POST':
	    # A comment was posted
	    comment_form = CommentForm(data=request.POST)
	    if comment_form.is_valid():
	        # Create Comment object but don't save to database yet
	        new_comment = comment_form.save(commit=False)
	        # Assign the current post to the comment
	        new_comment.post = post
	        # Save the comment to the database
	        new_comment.save()
	        messages.success(request, message='Ваш комментарий опубликован!')
	else:
		comment_form = CommentForm()
		ip = get_client_ip(request)
		counter, created = UniqueView.objects.get_or_create(post=post, ip=ip)

	return render(request,'blog/post/detail.html', {'post': post, 'comments': comments, 
													'comment_form': comment_form, 
													'similar_posts': similar_posts,
													'views': views,
													'comments': comments})


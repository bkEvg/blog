from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, DetailView
from .forms import CommentForm
from taggit.models import Tag
from django.db.models import Count
from django.db.models import F
from .helpers import get_client_ip
from .models import UniqueView, Comment
from django.db.models import Count
from django.contrib import messages
from django.db.models import Count
from django.template import RequestContext


class PostListView(ListView):

	""" Post list view """

	model = Post
	template_name = 'blog/post/list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		post_list = Post.objects.filter(status='published').order_by('-created')

		paginator = Paginator(post_list, 10) # Show 25 contacts per page.
		page_number = self.request.GET.get('page')
		context['page_obj'] = paginator.get_page(page_number)
		return context


class PostByTagView(PostListView):

	""" Post list by a tag """

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.kwargs['tag_slug']:
			context['tag'] = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
			context['posts'] = Post.objects.filter(tags__in=[context['tag']], status='published').order_by('-created')
		return context


class PostDetailView(DetailView):

	""" Post detail view """

	model = Post 
	context_object_name = 'post'
	template_name = 'blog/post/detail.html'

	def get_context_data(self, **kwargs):

		context = super().get_context_data(**kwargs)
		context['post'] = get_object_or_404(Post, slug=self.kwargs['slug'], status='published')
		context['post_tags_ids'] = context['post'].tags.values_list('id', flat=True)
		context['similar_posts'] = Post.objects.filter(tags__in=context['post_tags_ids'], status='published').exclude(id=context['post'].id)
		context['similar_posts'] = context['similar_posts'].annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
		context['comments'] = Comment.objects.filter(post=context['post'], active=True).order_by('-created')
		context['views'] = UniqueView.objects.filter(post=context['post'])
		# List of active comments for this post
		context['comments'] = context['post'].comments.filter(active=True)
		context['comment_form'] = CommentForm()
		context['ip'] = get_client_ip(self.request)
		counter, created = UniqueView.objects.get_or_create(post=context['post'], ip=context['ip'])
		return context

	def post(self, *args, **kwargs):
		self.object = self.get_object()
		comment_form = CommentForm(data=self.request.POST)
		context = super().get_context_data(**kwargs)
		if comment_form.is_valid():
			# Create Comment object but don't save to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.post = context['post']
			# Save the comment to the database
			new_comment.save()
			messages.success(self.request, message='Ваш комментарий опубликован!')
			url = self.request.META.get('HTTP_REFERER')
			return redirect(url)

		else:
			print('Form is not valid.')

def handler404(request, *args, **argv):
    return render(request,'blog/404.html')


def handler500(request, *args, **argv):
    return render(request, 'blog/500.html')

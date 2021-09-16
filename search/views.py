from django.shortcuts import render
from django.db.models import Q
from blog.models import Post
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def search(request):
	try:
		q = request.GET['q']
		posts = Post.objects.annotate(
			search=SearchVector('title', 'tags__name',),
		).filter(search=q, status='published').order_by('-created')

		# object_list = Post.objects.filter(status='published').order_by('-created')

		paginator = Paginator(posts, 10)  # posts in each page
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
				{
					'page': page,
					'posts': posts,
					'q': q,
					'search': True
				}
			)
		# return render(request, 'search/search.html', {'posts':posts})
	except KeyError:
		posts = []
		page = None
		return render(request,
				'blog/post/list.html',
				{
					'page': page,
					'posts': posts
				}
			)
	# results = BlogPost.objects.filter(
	# 	Q(title__icontains=your_search_query) | Q(intro__icontains=your_search_query) | Q(content__icontains=your_search_query)
	# )
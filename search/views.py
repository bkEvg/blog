from django.shortcuts import render
from django.db.models import Q
from blog.models import Post
from django.contrib.postgres.search import SearchVector
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



def search(request):
	if request.method == 'GET':
		try:
			q = request.GET['q']
			lookups= Q(title__icontains=q) | Q(tags__name__icontains=q) | Q(author__first_name__icontains=q) | Q(author__last_name__icontains=q)
			posts = Post.objects.filter(lookups)
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
						'page_obj': posts,
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
						'page_obj': posts
					}
				)
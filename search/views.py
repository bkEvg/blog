from django.shortcuts import render
from django.db.models import Q
from blog.models import Post
from django.contrib.postgres.search import SearchVector


def search(request):
	try:
		q = request.GET['q']
		posts = Post.objects.annotate(
			search=SearchVector('title', 'body'),
		).filter(search=q)
		return render(request, 'search/search.html', {'posts':posts})
	except KeyError:
	    return render(request, 'search/search.html')
	# results = BlogPost.objects.filter(
	# 	Q(title__icontains=your_search_query) | Q(intro__icontains=your_search_query) | Q(content__icontains=your_search_query)
	# )
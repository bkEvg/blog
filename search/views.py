from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from blog.models import Post


def search(request):
    q = request.GET.get('q', '')  # Получаем 'q' с пустой строкой по умолчанию
    lookups = Q(title__icontains=q) | Q(tags__name__icontains=q) | Q(
        author__first_name__icontains=q) | Q(author__last_name__icontains=q)

    posts = Post.objects.filter(lookups)
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, то берем первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница вне диапазона, берем последнюю страницу
        posts = paginator.page(paginator.num_pages)

    context = {
        'page': page,
        'page_obj': posts,
        'q': q,
        'search': True
    }

    return render(request, 'blog/post/list.html', context)

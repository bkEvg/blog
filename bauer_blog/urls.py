"""bauer_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path, include

from blog.sitemaps import PostSitemap, StaticViewSitemap

# Sitemap'ы для сайта, важно для SEO
sitemaps = {
    'main_page': StaticViewSitemap,
    'posts': PostSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),  # admin zone
    path('', include('blog.urls')),  # blog urls
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},  # sitemaps
         name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),  # paths for robots
    path('ckeditor/', include('ckeditor_uploader.urls')),  # ckeditor needs
    path('search/', include('search.urls'))  # search application
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )

# Обработка ошибок своими страницами
# Важно для SEO для для UX
handler404 = 'blog.views.handler404'
handler500 = 'blog.views.handler500'

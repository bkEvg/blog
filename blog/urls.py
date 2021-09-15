from django.urls import path
from . import views


urlpatterns = [
	path('', views.list, name='post_list'),
	path('tags/<tag_slug>/', views.list, name='post_list_by_tag'),
	path('posts/<day>/<month>/<year>/<post>/', views.detail, name='post_detail'),

]
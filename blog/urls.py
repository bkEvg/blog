from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('tags/<tag_slug>/', views.PostByTagView.as_view(),
         name='post_list_by_tag'),
    path('posts/<slug>/', views.PostDetailView.as_view(), name='post_detail'),

]
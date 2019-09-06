from django.conf.urls import url
from django.urls import path

from core import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # Первый вариант
    url(r'^post/(?P<post_id>[0-9]+)/$', views.post_detail, name='post_detail'),
    # Второй вариант
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/like/', views.like_post, name='like-post'),
    path('post/<int:post_id>/delete/', views.post_delete, name='delete-post'),
    path('post/create/', views.post_create, name='post_create'),
    path('feed/', views.feed, name='feed'),
]

# url(r'^$', views.index, name='index'),
# # Первый вариант
# url(r'^post/(?P<post_id>[0-9]+)/$', views.PostView.as_view(), name='post_detail'),
# # Второй вариант
# path('post/<int:post_id>/edit/', login_required(views.EditPostView.as_view()), name='post_edit'),
# path('post/<int:post_id>/like/', login_required(views.LikePostView.as_view()), name='like-post'),
# path('post/<int:post_id>/delete/', login_required(views.DeletePostView.as_view()), name='delete-post'),
# path('post/<int:post_id>/delete_success', TemplateView.as_view(template_name='core/delete_success.html'),
#      name='delete-post-success'),
# path('post/create/', views.CreatePostView.as_view(), name='post_create'),
# path('feed/', views.FeedView.as_view(), name='feed'),
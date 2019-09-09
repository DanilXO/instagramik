from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path
from django.views.generic import TemplateView

from core import views

app_name = 'core'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    # Первый вариант
    url(r'^post/(?P<post_id>[0-9]+)/$', views.PostView.as_view(), name='post_detail'),
    # Второй вариант
    path('post/<int:post_id>/edit/', login_required(views.EditPostView.as_view()), name='post_edit'),
    path('post/<int:post_id>/like/', login_required(views.LikePostView.as_view()), name='like_post'),
    path('post/<int:post_id>/delete/', login_required(views.DeletePostView.as_view()), name='delete_post'),
    path('post/<int:post_id>/delete_success', TemplateView.as_view(template_name='core/delete_success.html'),
         name='delete-post-success'),
    path('post/create/', views.CreatePostView.as_view(), name='post_create'),
    path('feed/', views.FeedView.as_view(), name='feed'),
]


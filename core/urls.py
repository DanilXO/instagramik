from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from django.views.generic import TemplateView

from core import views
from core.views import SignupView, EditProfileView, AddRemoveFriend, ProfileView, logout_view, LoginView

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

from django.contrib.auth.views import PasswordResetDoneView, PasswordResetView, PasswordResetConfirmView, \
    PasswordResetCompleteView

urlpatterns += [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('<int:user_id>/profile/', ProfileView.as_view(), name='profile'),
    path('<int:user_id>/profile/add_remove_friend', login_required(AddRemoveFriend.as_view()),
         name='add-remove-friend'),
    path('<int:user_id>/profile/edit', login_required(EditProfileView.as_view()), name='edit-profile'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('password_reset/', PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done'),
                                                      template_name='my_auth/password_reset.html'),
         name='password_reset'),

    path('password_reset/done', PasswordResetDoneView.as_view(template_name='my_auth/password_reset_done.html'),
         name='password_reset_done'),

    path('password_reset/<str:uidb64>/<slug:token>', PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),

    path('password_reset/complete', PasswordResetCompleteView.as_view(), name='password_reset_complete')
]


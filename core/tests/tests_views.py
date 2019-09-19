import codecs
import os
import tempfile
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from core.forms import CommentForm, PostForm
from core.models import Post, Comment


class TestIndexView(TestCase):

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        dir_ = os.path.dirname(os.path.abspath(__file__))
        image = os.path.join(dir_, 'static', 'test.png')
        f = codecs.open(image, encoding='base64')
        self.image = SimpleUploadedFile(f.name, f.read())
        f.close()

    def test_index_page_without_posts(self):
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Постов нет')

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_index_page_with_post(self):
        user = User.objects.create_user(username='username', password='pass1234')
        post = Post.objects.create(author=user, description='', image=self.image)
        response = self.client.get(reverse('core:index'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['popular_posts'], [post], transform=lambda x: x)


class TestFeedView(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='1234')
        dir_ = os.path.dirname(os.path.abspath(__file__))
        image = os.path.join(dir_, 'static', 'test.png')
        f = codecs.open(image, encoding='base64')
        self.image = SimpleUploadedFile(f.name, f.read())
        f.close()

    def test_feed_without_login(self):
        response = self.client.get(reverse('core:feed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Чтобы просматривать ленту друзей, вам нужно')

    def test_feed_without_friends(self):
        self.client.login(username='user', password='1234')
        response = self.client.get(reverse('core:feed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'У вас пока что нет друзей')

    def test_feed_without_posts(self):
        user2 = User.objects.create_user(username='user2', password='1234')
        self.user.user_profile.friends.add(user2)
        self.client.login(username='user', password='1234')
        response = self.client.get(reverse('core:feed'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Лента пуста')
        self.assertQuerysetEqual(response.context['feed'], [])

    def test_feed_with_posts(self):
        friend = User.objects.create_user(username='user3', password='1234')
        self.user.user_profile.friends.add(friend)
        post = Post.objects.create(author=friend, description='', image=self.image)
        self.client.login(username='user', password='1234')
        response = self.client.get(reverse('core:feed'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['feed'], [post], transform = lambda x: x)

# TODO: Тесты не рабочие. просто пример из подобного проекта
# class TestPostView(TestCase):
#
#     @override_settings(MEDIA_ROOT=tempfile.gettempdir())
#     def setUp(self):
#         self.user = User.objects.create_user(username='user', password='1234')
#         dir_ = os.path.dirname(os.path.abspath(__file__))
#         image = os.path.join(dir_, 'static', 'test.png')
#         f = codecs.open(image, encoding='base64')
#         self.image = SimpleUploadedFile(f.name, f.read())
#         f.close()
#
#     def test_wrong_post_id(self):
#         response = self.client.get(reverse('core:post', args=(30,)))
#         self.assertEqual(response.status_code, 404)
#
#     def test_right_post_id(self):
#         post = Post.objects.create(author=self.user, description='', image=self.image)
#         response = self.client.get(reverse('core:post', args=(post.id,)))
#         self.assertEqual(response.status_code, 200)
#         self.assertAlmostEqual(response.context['post_detail'], post)
#
#     def test_no_login_no_comment_form(self):
#         post = Post.objects.create(author=self.user, description='', image=self.image)
#         response = self.client.get(reverse('core:post', args=(post.id,)))
#         self.assertEqual(response.status_code, 200)
#         self.assertIsNone(response.context['comment_form'])
#         self.assertContains(response, 'Комментарии только для зарегистрированных пользователей')
#
#     def test_with_login_with_comment_form(self):
#         post = Post.objects.create(author=self.user, description='', image=self.image)
#         self.client.login(username='user', password='1234')
#         response = self.client.get(reverse('core:post', args=(post.id,)))
#         self.assertEqual(response.status_code, 200)
#         self.assertIs(response.context['comment_form'], CommentForm)
#         self.assertContains(response, 'Комментариев нет. Вы можете стать первым.')
#
#     def test_post_with_comments(self):
#         post = Post.objects.create(author=self.user, description='', image=self.image)
#         comment = Comment.objects.create(author=self.user, text='hello', in_post=post)
#         self.client.login(username='user', password='1234')
#         response = self.client.get(reverse('core:post', args=(post.id,)))
#         self.assertEqual(response.status_code, 200)
#         self.assertQuerysetEqual(response.context['comments'], [comment], transform=lambda x: x)
#
#
# class TestCreatePostView(TestCase):
#
#     def test_create_post_without_login(self):
#         response = self.client.get(reverse('core:post_create'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, 'Чтобы создавать посты, вам нужно')
#
#     def test_create_post_form_with_login(self):
#         user = User.objects.create_user(username='user', password='password')
#         self.client.login(username='user', password='password')
#         response = self.client.get(reverse('core:post_create'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, '<form')
#         self.assertIsInstance(response.context['form'], PostForm)
#
#
# class TestLikePostView(TestCase):
#
#     @override_settings(MEDIA_ROOT=tempfile.gettempdir())
#     def setUp(self):
#         dir_ = os.path.dirname(os.path.abspath(__file__))
#         image = os.path.join(dir_, 'static', 'test.png')
#         f = codecs.open(image, encoding='base64')
#         self.image = SimpleUploadedFile(f.name, f.read())
#         f.close()
#         user = User.objects.create_user(username='user', password='1234')
#         self.post = Post.objects.create(author=user, description='', image=self.image)
#
#     def test_like_post_without_login(self):
#         response = self.client.post(reverse("core:like_post", args=(self.post.id,)))
#         self.assertEqual(response.status_code, 302)
#
#     def test_like_post_with_login(self):
#         self.client.login(username='user', password='1234')
#         response = self.client.get(reverse('core:like_post', args=(self.post.id,)))
#         self.assertEqual(self.post.get_likes, 1)
#         response = self.client.get(reverse('core:like_post', args=(self.post.id,)))
#         self.assertEqual(self.post.get_likes, 0)
#
#
# class EditPostView(TestCase):
#
#     @override_settings(MEDIA_ROOT=tempfile.gettempdir())
#     def setUp(self):
#         dir_ = os.path.dirname(os.path.abspath(__file__))
#         image = os.path.join(dir_, 'static', 'test.png')
#         f = codecs.open(image, encoding='base64')
#         self.image = SimpleUploadedFile(f.name, f.read())
#         f.close()
#         user = User.objects.create_user(username='user', password='1234')
#         self.post = Post.objects.create(author=user, description='', image=self.image)
#
#     def test_editpost_if_not_author(self):
#         user = User.objects.create_user(username='test', password='1234')
#         self.client.login(username='test', password='1234')
#         response = self.client.get(reverse('core:post_edit', args=(self.post.id,)))
#         self.assertEqual(response.status_code, 404)
#
#     def test_editpost_if_author(self):
#         self.client.login(username='user', password='1234')
#         response = self.client.get(reverse('core:post_edit', args=(self.post.id,)))
#         self.assertEqual(response.status_code, 200)

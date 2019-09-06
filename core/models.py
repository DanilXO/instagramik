from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.utils import timezone


def user_directory_path(instance, filename):
    return "user_{0}/posts/{1}".format(instance.author.id, filename)


def user_avatar_path(instance, filename):
    return "user_{0}/avatar/{1}".format(instance.user.id, filename)


class Profile(models.Model):
    """ Модель профиля.
    С использованием django-user. Самый простой способ расширить стандартную модель пользователя"""
    # TODO: Подробно о стратегиях расширения Django User Model читайте здесь: https://habr.com/ru/post/313764/
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    birth_date = models.DateField('Date of Birth', null=True, blank=True)
    about = models.TextField(max_length=500, blank=True)
    avatar = models.ImageField(upload_to=user_avatar_path, default=None)
    friends = models.ManyToManyField(User, related_name='friends', blank=True)

    def __str__(self):
        return str(self.user.username)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_profile.save()


class Post(models.Model):
    """
    Пост пользователя с картинкой
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000, blank=True)
    image = models.ImageField(upload_to=user_directory_path)
    likes = models.ManyToManyField(User, related_name='users_likes_it', blank=True)
    date_pub = models.DateTimeField(default=timezone.now)
    date_edit = models.DateTimeField(default=timezone.now)

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url

    @property
    def get_likes(self):
        return self.likes.count()

    def __str__(self):
        return "author {0} description {1}".format(self.author.username, self.description)


class Comment(models.Model):
    """
    Коментарий к посту
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=700, blank=False)
    in_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_publish = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "{0} : {1}".format(self.author, self.text[:10] + "...")


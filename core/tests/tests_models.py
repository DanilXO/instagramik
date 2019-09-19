import datetime
import unittest

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase


class TestProfileModels(TestCase):
    def setUp(self):
        self.user = User(username='test', first_name='test', last_name='testov', email='test@test.com')
        self.user.save()
        super().setUp()

    def test_birth_date_with_future_date(self):
        with self.assertRaises(ValidationError):
            self.user.user_profile.birth_date = datetime.datetime.now() + datetime.timedelta(days=1)
            self.user.user_profile.save()

    @unittest.expectedFailure
    def test_birth_date_with_past_date(self):
        with self.assertRaises(ValidationError):
            self.user.user_profile.birth_date = datetime.datetime.now() - datetime.timedelta(weeks=1800)
            self.user.user_profile.save()

    def test_add_friends(self):
        """ Проверяет, корректность работы добавления в друзья """
        ...

    def test_create_profile_with_user(self):
        """ Проверяет, что создается профиль при создании пользователя """
        ...


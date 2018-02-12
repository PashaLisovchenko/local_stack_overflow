from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from accounts.forms import RegisterForm


class AccountViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='pasha', password='12345')
        user.save()

    def test_user_login(self):
        user = User.objects.get(username='pasha')
        url = reverse('accounts:login')
        data = {'username': user.username, 'password': '12345'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        data = {'username': "asd", 'password': '1234eee5'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        data = {'username': user.username, 'password': '12345', 'next': '/'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        login = self.client.login(username='pasha', password='12345')
        self.assertTrue(login)
        url = reverse('accounts:logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_create_user(self):
        url = reverse('accounts:signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        data = {'username': 'testuser1', 'password1': 'qwerty123', 'password2': 'qwerty123', 'email': 'testuser1@gmail.com'}
        self.client.post(url, data)
        user = User.objects.filter(username='testuser1').exists()
        self.assertTrue(user)


class ProfileViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='testuser2', password='12345')
        user.save()

    def test_user_have_profile(self):
        user = User.objects.get(username='testuser2')
        kwargs = {'id': user.id}
        url = reverse("accounts:profile", kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        kwargs = {'id': '123'}
        url = reverse("accounts:profile", kwargs=kwargs)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

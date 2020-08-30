from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth.models import User
from apps.users.models.profile import UserProfile


class UsersAPITests(APITestCase):
    def test_get_token(self):
        """
        Test that user can get authorization 'token'
        """
        user_data = {
            'username': 'Einstein',
            'password': 'strongpsw123',
            'email': 'test@company.com',
        }
        count_user_before = User.objects.count()
        count_token_before = Token.objects.count()

        url = '/api/users/'
        response = self.client.post(url, user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('token' in response.data)

        self.assertEqual(User.objects.count(), count_user_before + 1)
        self.assertEqual(Token.objects.count(), count_token_before + 1)

    def test_create_profile(self):
        """
        Test that profile is created when user signs up
        """
        user_data = {
            'username': 'Einstein',
            'password': 'strongpsw123',
            'email': 'test@company.com',
        }
        count_profiles_before = UserProfile.objects.count()

        url = '/api/users/'
        response = self.client.post(url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), count_profiles_before + 1)

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.auth.models import User
from apps.users.models.profile import UserProfile


class UsersAPITests(APITestCase):
    def setUp(self):
        test_user1_data = {
            'username': 'Testuser',
            'password': 'strongpsw123',
            'email': 'Testuser@company.com',
        }
        response = self.client.post('/api/users/', test_user1_data, format='json')
        self.test_user1_response = response.data

        test_user2 = User.objects.create(username='Linus', password='linux123', email='email@com.com')
        self.test_user2_token = 'Token ' + Token.objects.create(user=test_user2).key

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

    def test_delete_profile(self):
        """
        Test that user can delete its profile
        """
        user_data = {
            'username': 'Einstein',
            'password': 'strongpsw123',
            'email': 'test@company.com',
        }
        count_profiles_before = UserProfile.objects.count()
        count_users_before = User.objects.count()
        client = APIClient()

        response = client.post('/api/users/', user_data, format='json')
        token = 'Token ' + response.data['token']
        client.credentials(HTTP_AUTHORIZATION=token)
        url = f"/api/profile/{response.data['id']}/"

        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(count_users_before, User.objects.count())
        self.assertEqual(count_profiles_before, UserProfile.objects.count())

    def test_delete_profile_by_no_owner(self):
        """
        Test that user cannot delete others profile
        """
        user_data = {
            'username': 'Einstein',
            'password': 'strongpsw123',
            'email': 'test@company.com',
        }
        client = APIClient()

        response = client.post('/api/users/', user_data, format='json')
        token = 'Token ' + response.data['token']
        client.credentials(HTTP_AUTHORIZATION=self.test_user2_token)
        url = f"/api/profile/{response.data['id']}/"

        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_profile(self):
        """
        Test that every user can retrieve profile
        """
        url = f"/api/profile/{self.test_user1_response['id']}/"

        response = self.client.get(url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertTrue('id' and 'user' and 'bio' in response.data)

    def test_update_profile_by_non_owner(self):
        """
        Test that non owner cannot update other profile
        """
        url = f"/api/profile/{self.test_user1_response['id']}/"
        send_data = {
            "id": {self.test_user1_response['id']},
            "user": {self.test_user1_response['id']},
            "bio": "Testing text",
            "img": "",
            "following": []
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user2_token)

        response = client.put(url, send_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.patch(url, send_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

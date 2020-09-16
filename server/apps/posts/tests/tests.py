from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User

from apps.posts.models.posts import Post
from apps.users.models.profile import UserProfile


class PostsAPITests(APITestCase):
    def setUp(self):
        self.test_user1 = User.objects.create(username='Guido', password='python123', email='emails@com.com')
        self.test_user1_token = 'Token ' + Token.objects.create(user=self.test_user1).key

        self.test_user2 = User.objects.create(username='Linus', password='linux123', email='email@com.com')
        self.test_user2_token = 'Token ' + Token.objects.create(user=self.test_user2).key

        profile = UserProfile.objects.get(user=self.test_user1)

        Post.objects.create(
            title='some title',
            content='hello',
            content_type=ContentType.objects.get_for_id(9),
            object_id=profile.id,
            profile=profile,
        )

    def test_create_post(self):
        """
        Test that user can create post on its profile.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        count_posts_before = Post.objects.count()
        profile = self.test_user1.profile.get()
        send_post_data = {
            'content': 'hello',
            'title': 'Testing',
            'content_type': 9,
            'object_id': profile.id,
        }

        response = client.post('/api/posts/', send_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), count_posts_before + 1)

    def test_create_post_without_token(self):
        """
        Test that not authenticated user cannot create post
        """
        count_posts_before = Post.objects.count()
        send_post_data = {
            'content': 'hello',
            'title': 'Testing',
            'content_object': self.test_user1.profile.get().__str__(),
        }

        response = self.client.post('/api/posts/', send_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(count_posts_before, Post.objects.count())

    def test_retrieve_post(self):
        """
        Test that user can retrieve post
        """
        url = f'/api/posts/{Post.objects.first().id}/'

        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_post_with_token(self):
        """
        Test that user with token can retrieve post
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        url = f'/api/posts/{Post.objects.first().id}/'

        response = client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_by_owner(self):
        """
        Test that user can update its post.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        profile = self.test_user1.profile.get()
        send_post_data = {
            'content': 'hello',
            'title': 'Testing',
            'content_type': 9,
            'object_id': profile.id,
        }

        response = client.post('/api/posts/', send_post_data, format='json')

        url = f"/api/posts/{response.data['id']}/"
        send_post_data['content'] = 'Hola!'
        response = client.put(url, send_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(send_post_data['content'], response.data['content'])

        updated_post_data = {
            'content': 'Ciao',
            'title': 'Testing',
            'content_object': self.test_user1.profile.get().__str__(),
        }
        response = client.patch(url, updated_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_post_data['content'], response.data['content'])

    def test_update_post_by_not_owner(self):
        """
        Test that user cannot update others post
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        profile = self.test_user1.profile.get()
        send_post_data = {
            'content': 'hello',
            'title': 'Testing',
            'content_type': 9,
            'object_id': profile.id,
        }

        response = client.post('/api/posts/', send_post_data, format='json')

        client.credentials(HTTP_AUTHORIZATION=self.test_user2_token)
        url = f"/api/posts/{response.data['id']}/"
        send_post_data['content'] = 'Hola'
        response = client.put(url, send_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = client.patch(url, send_post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_by_owner(self):
        """
        Test that user can delete its post.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        profile = self.test_user1.profile.get()
        send_post_data = {
            'content': 'hello',
            'title': 'Testing',
            'content_type': 9,
            'object_id': profile.id,
        }
        response = client.post('/api/posts/', send_post_data, format='json')
        url = f"/api/posts/{response.data['id']}/"

        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_others_post(self):
        """
        Test that user cannot delete others post.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        profile = self.test_user1.profile.get()
        send_post_data = {
            'content': 'hello',
            'title': 'Testing',
            'content_type': 9,
            'object_id': profile.id,
        }
        response = client.post('/api/posts/', send_post_data, format='json')
        url = f"/api/posts/{response.data['id']}/"

        client.credentials(HTTP_AUTHORIZATION=self.test_user2_token)
        response = client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

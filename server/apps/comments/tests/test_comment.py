import io

from PIL import Image as IMG

from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from rest_framework import status

from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.files import File as DjangoFile

from apps.comments.models.comment import Comment
from apps.posts.models.posts import Post
from apps.image.models.image import Image


class CommentAPITestCase(APITestCase):
    def generate_photo_file(self):
        file = io.BytesIO()
        image = IMG.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def setUp(self):
        self.test_user1 = User.objects.create(username='Guido', password='python123', email='emails@com.com')
        self.test_user1_token = 'Token ' + Token.objects.create(user=self.test_user1).key

        self.test_user2 = User.objects.create(username='Linus', password='linux123', email='email@com.com')
        self.test_user2_token = 'Token ' + Token.objects.create(user=self.test_user2).key

        post = Post.objects.create(
            profile=self.test_user1.profile.get(),
            title='Title',
            content='Hello, Ouvert!',
            content_object=self.test_user2.profile.get()
        )
        image = Image(
            profile=self.test_user1.profile.get(),
            image=DjangoFile(self.generate_photo_file()),
            content_type=ContentType.objects.get_for_id(10),
            object_id=post.id,
        )
        image.save()

    def test_comment_post(self):
        """
        Test that authenticated user can comment a post.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        comment_quantity_before = Comment.objects.count()
        comment_data = {
            'content': 'Hello, Ouvert!',
            'content_type': 10,
            'object_id': Post.objects.last().id
        }
        url = reverse('comments-list')

        response = client.post(url, comment_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('content' in response.data)
        self.assertTrue('content_type' in response.data)
        self.assertTrue('object_id' in response.data)
        self.assertTrue('profile' in response.data)
        self.assertEqual(Comment.objects.count(), comment_quantity_before + 1)

    def test_comment_post_by_not_authenticated_user(self):
        """
        Test that not authenticated user cannot comment a post.
        """
        client = APIClient()
        comment_quantity_before = Comment.objects.count()
        comment_data = {
            'content': 'Hello, Ouvert!',
            'content_type': 10,
            'object_id': Post.objects.last().id
        }
        url = reverse('comments-list')

        response = client.post(url, comment_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Comment.objects.count(), comment_quantity_before)

    def test_comment_image(self):
        """
        Test that authenticated user can comment an image.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        comment_quantity_before = Comment.objects.count()
        comment_data = {
            'content': 'Hello, Ouvert!',
            'content_type': 11,
            'object_id': Image.objects.last().id
        }
        url = reverse('comments-list')

        response = client.post(url, comment_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('content' in response.data)
        self.assertTrue('content_type' in response.data)
        self.assertTrue('object_id' in response.data)
        self.assertTrue('profile' in response.data)
        self.assertEqual(Comment.objects.count(), comment_quantity_before + 1)

    def test_comment_image_by_not_authenticated_user(self):
        """
        Test that not authenticated user cannot comment an image.
        """
        comment_quantity_before = Comment.objects.count()
        comment_data = {
            'content': 'Hello, Ouvert!',
            'content_type': 11,
            'object_id': Image.objects.last().id
        }
        url = reverse('comments-list')

        response = self.client.post(url, comment_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Comment.objects.count(), comment_quantity_before)

    def test_delete_image(self):
        """
        Test that user can delete its profile.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        comment_data = {
            'content': 'Hello, Ouvert!',
            'content_type': 11,
            'object_id': Image.objects.last().id
        }
        url = reverse('comments-list')

        response = client.post(url, comment_data, format='json')
        comment_quantity_before = Comment.objects.count()
        url = f"{url}{response.data['id']}/"

        response = client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), comment_quantity_before - 1)

    def test_delete_image_by_not_owner(self):
        """
        Test that user cannot delete others profile.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        comment_data = {
            'content': 'Hello, Ouvert!',
            'content_type': 11,
            'object_id': Image.objects.last().id
        }
        url = reverse('comments-list')

        response = client.post(url, comment_data, format='json')
        comment_quantity_before = Comment.objects.count()
        url = f"{url}{response.data['id']}/"

        client.credentials(HTTP_AUTHORIZATION=self.test_user2_token)
        response = client.delete(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Comment.objects.count(), comment_quantity_before)

    def test_put_request_to_image(self):
        """
        Test that user can send `PUT` request to its profile.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        comment_data = {
            'content': 'Hello, Ouvert!',
            'content_type': 11,
            'object_id': Image.objects.last().id
        }
        url = reverse('comments-list')

        response = client.post(url, comment_data, format='json')
        comment_quantity_before = Comment.objects.count()
        url = f"{url}{response.data['id']}/"
        comment_data['content'] = 'Updated content field!'

        response = client.put(url, comment_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), comment_quantity_before)

    def test_put_request_to_image_by_not_owner(self):
        """
        Test that user cannot send `PUT` request to others profile.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        comment_data = {
            'content': 'Hello, Ouvert!',
            'content_type': 11,
            'object_id': Image.objects.last().id
        }
        url = reverse('comments-list')

        response = client.post(url, comment_data, format='json')
        comment_quantity_before = Comment.objects.count()
        url = f"{url}{response.data['id']}/"
        comment_data['content'] = 'Updated content field!'

        client.credentials(HTTP_AUTHORIZATION=self.test_user2_token)
        response = client.put(url, comment_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        checking_response = self.client.get(url, format='json')
        self.assertNotEqual(checking_response.data['content'], comment_data['content'])
        self.assertEqual(Comment.objects.count(), comment_quantity_before)

    def test_patch_request_to_image(self):
        """
        Test that user can send `PATCH` request to its profile.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        comment_data = {
            'content': 'Hello, Ouvert!',
            'content_type': 11,
            'object_id': Image.objects.last().id
        }
        url = reverse('comments-list')

        response = client.post(url, comment_data, format='json')
        comment_quantity_before = Comment.objects.count()
        url = f"{url}{response.data['id']}/"
        comment_data['content'] = 'Updated content field!'

        response = client.patch(url, comment_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        checking_response = self.client.get(url, format='json')
        self.assertEqual(checking_response.data['content'], comment_data['content'])

        self.assertEqual(Comment.objects.count(), comment_quantity_before)

    def test_patch_request_to_image_by_not_owner(self):
        """
        Test that user cannot send `PATCH` request to others profile.
        """
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=self.test_user1_token)
        comment_data = {
            'content': 'Hello, Ouvert!',
            'content_type': 11,
            'object_id': Image.objects.last().id
        }
        url = reverse('comments-list')

        response = client.post(url, comment_data, format='json')
        comment_quantity_before = Comment.objects.count()
        url = f"{url}{response.data['id']}/"
        comment_data['content'] = 'Updated content field!'

        client.credentials(HTTP_AUTHORIZATION=self.test_user2_token)
        response = client.patch(url, comment_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        checking_response = self.client.get(url, format='json')
        self.assertNotEqual(checking_response.data['content'], comment_data['content'])
        self.assertEqual(Comment.objects.count(), comment_quantity_before)


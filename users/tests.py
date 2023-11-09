from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .authentication import get_tokens_for_user
from .models import User
from .serializers import UserSerializer


class TokenTestCase(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword')

    def test_get_tokens_for_user(self):
        # Call the get_tokens_for_user function for the created user
        tokens = get_tokens_for_user(self.user)

        # Check that the received tokens are strings
        self.assertIsInstance(tokens['refresh'], str)
        self.assertIsInstance(tokens['access'], str)

        # Check token validity
        refresh_token = RefreshToken(tokens['refresh'])
        access_token = AccessToken(tokens['access'])

        # Check that tokens are not expired
        self.assertGreater(refresh_token['exp'], datetime.now().timestamp())
        self.assertGreater(access_token['exp'], datetime.now().timestamp())


class UserCreateAPIViewTestCase(APITestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser',
                                             password='testpassword',
                                             email='testuser@example.com')
        self.client = APIClient()

    def test_create_user(self):
        url = '/user/create/'
        data = {
            "id": 1,
            "password": "454125",
            "is_superuser": True,
            "username": "ivan2",
            "first_name": "",
            "last_name": "",
            "is_staff": True,
            "date_joined": "2023-11-04T01:29:40.967290+03:00",
            "email": "ivan2@skypro.ru",
            "roles": "Member",
            "is_active": True,
            "groups": [],
            "user_permissions": []
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.first().username, 'testuser')
        self.assertEqual(User.objects.first().email, 'testuser@example.com')

    def test_create_user_with_tokens(self):
        url = '/user/create/'
        data = {
            "id": 1,
            "password": "454125",
            "is_superuser": True,
            "username": "ivan2",
            "first_name": "",
            "last_name": "",
            "is_staff": True,
            "date_joined": "2023-11-04T01:29:40.967290+03:00",
            "email": "ivan2@skypro.ru",
            "roles": "Member",
            "is_active": True,
            "groups": [],
            "user_permissions": []
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_create_user_with_existing_username(self):
        User.objects.create_user(username='testuser1',
                                 email='testuser1@example.com',
                                 password='testpassword')
        url = '/user/create/'  # Updated URL
        self.client = APIClient()
        data = {
            "id": 1,
            "password": "454125",
            "is_superuser": True,
            "username": "testuser1",
            "first_name": "",
            "last_name": "",
            "is_staff": True,
            "date_joined": "2023-11-04T01:29:40.967290+03:00",
            "email": "ivan2@skypro.ru",
            "roles": "Member",
            "is_active": True,
            "groups": [],
            "user_permissions": []
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 2)


class UserSerializerTest(APITestCase):
    def test_create_user(self):
        data = {
            "id": 1,
            "password": "454125",
            "is_superuser": True,
            "username": "testuser1",
            "first_name": "",
            "last_name": "",
            "is_staff": True,
            "date_joined": "2023-11-04T01:29:40.967290+03:00",
            "email": "ivan2@skypro.ru",
            "roles": "Member",
            "is_active": True,
            "groups": [],
            "user_permissions": []
        }
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()

        self.assertEqual(user.username, 'testuser1')
        self.assertEqual(user.email, 'ivan2@skypro.ru')
        self.assertTrue(user.check_password('454125'))

    def test_update_user(self):
        user = User.objects.create(username='testuser',
                                   password='testpassword')

        data = {
            "id": 1,
            "password": "454125",
            "is_superuser": True,
            "username": "testuser1",
            "first_name": "",
            "last_name": "",
            "is_staff": True,
            "date_joined": "2023-11-04T01:29:40.967290+03:00",
            "email": "ivan2@skypro.ru",
            "roles": "Member",
            "is_active": True,
            "groups": [],
            "user_permissions": []
        }
        serializer = UserSerializer(instance=user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()

        self.assertEqual(user.username, updated_user.username)
        self.assertEqual(updated_user.email, 'ivan2@skypro.ru')
        self.assertTrue(updated_user.check_password('454125'))

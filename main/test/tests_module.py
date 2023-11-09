from django.test import TestCase
from main.serializers import ModuleSerializer
from main.models import Module
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

import json

from rest_framework.test import APIClient


class ModuleSerializerTests(TestCase):
    """Класс ModuleSerializerTests тестирует функциональности
    ModuleSerializer. Проверяет, что все указанные поля
    `fields` в `ModuleSerializer`, присутствуют в сериализованных
    данных. Также Проверяет, что данные в сериализаторе соответствуют
    данным модуля, который мы создали в `setUp`."""

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.module_data = Module(
            user=self.user,
            number=1,
            title='Module 1',
            description='Module 1 description'
        )

        self.module = Module.objects.create(
            user=self.module_data.user,
            number=self.module_data.number,
            title=self.module_data.title,
            description=self.module_data.description
        )
        self.serializer = ModuleSerializer(instance=self.module)

    def test_module_serializer_fields(self):
        self.assertEqual(set(self.serializer.fields.keys()),
                         set(['id', 'user', 'number', 'title',
                              'description', 'is_paid']))

    def test_module_serializer_data(self):
        data = self.serializer.data
        self.assertEqual(data['number'], self.module_data.number)
        self.assertEqual(data['title'], self.module_data.title)
        self.assertEqual(data['description'], self.module_data.description)
        self.assertEqual(data['is_paid'], self.module.is_paid)


class ModuleModelTests(TestCase):
    """Класс ModuleModelTests тестирует
    функциональности созданной модели Model.
    Проверяет, что все поля модели `Module`
    правильно сохранены, а также проверяет,
    что строковое представление модуля
    соответствует его названию."""

    def setUp(self):
        self.user = User.objects.create(username='testuser')
        self.module = Module.objects.create(
            user=self.user,
            number=1,
            title='Module 1',
            description='Module 1 description'
        )

    def test_module_model_fields(self):
        self.assertEqual(self.module.user, self.user)
        self.assertEqual(self.module.number, 1)
        self.assertEqual(self.module.title, 'Module 1')
        self.assertEqual(self.module.description, 'Module 1 description')

    def test_module_model_string_representation(self):
        self.assertEqual(str(self.module), 'Module 1')


class ModuleCreateAPIViewTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', password='testpassword'
        )
        self.module = Module.objects.create(
            user=self.superuser,
            number=1,
            title='Module 1',
            description='Module 1 description',
            is_paid=True
        )

    def test_module_create_api_view(self):
        url = '/module/create/'
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(url, data={'title': 'Module 1',
                                               'number': 1,
                                               'description': 'Module 1 '
                                                              'description',
                                               'user': self.superuser.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Module.objects.count(), 2)


class ModuleUpdateAPIViewTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', password='testpassword'
        )
        self.module = Module.objects.create(
            user=self.superuser,
            number=1,
            title='Module 1',
            description='Module 1 description',
            is_paid=True
        )

    def test_module_update_api_view(self):
        url = f'/module/update/{self.module.id}/'
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        data = {'number': 1, 'user': self.superuser.id,
                'title': 'Updated Title',
                'description': 'Updated Description'}
        response = self.client.put(url, data=json.dumps(data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ModuleDestroyAPIViewTest(APITestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            username='admin', password='testpassword'
        )
        self.module = Module.objects.create(
            user=self.superuser,
            number=1,
            title='Module 1',
            description='Module 1 description',
            is_paid=True
        )

    def test_module_destroy_api_view(self):
        url = f'/module/delete/{self.module.id}/'
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ModuleRetrieveAPIViewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.module = Module.objects.create(
            user=self.user,
            number=1,
            title='Module 1',
            description='Module 1 description',
            is_paid=True
        )
        self.client = APIClient()

    def test_module_retrieve_paid(self):
        self.client = APIClient()
        """
        Test retrieving a paid module
        """
        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/module/{self.module.pk}/')

        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(response.data,
                         ModuleSerializer(self.module).data)

    def test_module_retrieve_not_paid(self):
        self.client = APIClient()
        """
        Test retrieving a not paid module
        """
        self.client.force_authenticate(user=self.user)

        # Set module is_paid to False
        self.module.is_paid = False
        self.module.save()

        response = self.client.get(f'/module/{self.module.pk}/')

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You are not allowed'
                                                  'to view this module '
                                                  'in detail.')

    def test_module_retrieve_unauthenticated(self):
        """
        Test retrieving a module without authentication
        """
        response = self.client.get(f'/module/{self.module.pk}/')

        self.assertEqual(response.status_code,
                         status.HTTP_401_UNAUTHORIZED)

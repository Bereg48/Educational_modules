from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Module
from django.test import TestCase

from .serializers import ModuleSerializer


class ModuleTests(APITestCase):
    """Класс ModuleTests тестирует функциональности CRUD"""

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.module = Module.objects.create(user=self.user, number=1, title='Module 1', description='Module 1 description')

    def test_module_list(self):
        """Тестирование просмотра модулей"""
        url = reverse('module-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_module_create(self):
        """Тестирование создания модулей"""
        url = reverse('module-create')
        data = {
            'number': 2,
            'title': 'Module 2',
            'description': 'Module 2 description'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_module_retrieve(self):
        """Тестирование просмотра отдельных модулей"""
        url = reverse('module-retrieve', kwargs={'pk': self.module.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_module_update(self):
        """Тестирование обновление модулей"""
        url = reverse('module-update', kwargs={'pk': self.module.pk})
        data = {
            'number': 10
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.module.refresh_from_db()
        self.assertEqual(self.module.number, 10)

    def test_module_destroy(self):
        """Тестирование удаления модулей"""
        url = reverse('module-destroy', kwargs={'pk': self.module.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ModuleSerializerTests(TestCase):
    """Класс ModuleSerializerTests тестирует функциональности ModuleSerializer. Проверяет, что все указанные поля
    `fields` в `ModuleSerializer`, присутствуют в сериализованных данных. Также Проверяет, что данные
    в сериализаторе соответствуют данным модуля, который мы создали в `setUp`."""

    def setUp(self):
        self.module_data = {
            'number': 1,
            'title': 'Module 1',
            'description': 'Module 1 description'
        }
        self.module = Module.objects.create(**self.module_data)
        self.serializer = ModuleSerializer(instance=self.module)

    def test_module_serializer_fields(self):
        self.assertEqual(set(self.serializer.fields.keys()),
                         set(['id', 'number', 'title', 'description', 'created_at', 'updated_at']))

    def test_module_serializer_data(self):
        data = self.serializer.data
        self.assertEqual(data['number'], self.module_data['number'])
        self.assertEqual(data['title'], self.module_data['title'])
        self.assertEqual(data['description'], self.module_data['description'])
        self.assertEqual(data['created_at'], self.module.created_at.isoformat())
        self.assertEqual(data['updated_at'], self.module.updated_at.isoformat())


class ModuleModelTests(TestCase):
    """Класс ModuleModelTests тестирует функциональности созданной модели Model.
    Проверяет, что все поля модели `Module` правильно сохранены, а также проверяет,
    что строковое представление модуля соответствует его названию."""

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
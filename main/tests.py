from rest_framework.exceptions import ValidationError
from main.validators import TitleValidator, validator_description_words
from django.test import TestCase
from .serializers import ModuleSerializer
import unittest
from main.models import Module, Section
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from django.urls import reverse


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
                         set(['id', 'user', 'number', 'title','description', 'is_paid']))

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


class TestTitleValidator(unittest.TestCase):
    def test_valid_title(self):
        validator = TitleValidator(field='title')
        value = {'title': 'Invalid Title!'}
        with self.assertRaises(ValidationError):
            validator(value)

    def test_invalid_title(self):
        validator = TitleValidator(field='title')
        value = {'title': 'invalid_title!@#$'}
        with self.assertRaises(ValidationError):
            validator(value)


class TestDescriptionWordsValidator(unittest.TestCase):
    def test_valid_description(self):
        value = 'This is a valid description'
        self.assertIsNone(validator_description_words(value))

    def test_invalid_description(self):
        value = 'This description contains a scam word: война'
        with self.assertRaises(ValidationError):
            validator_description_words(value)


class SectionListAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.module = Module.objects.create(
            user=self.user,
            number=1,
            title='Module 1',
            description='Module 1 description',
            is_paid=True
        )
        self.section = Section.objects.create(
            number=1,
            title='Test Section',
            module=self.module
        )

    def test_section_list_api_view(self):
        url = reverse('main:section-list')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.section.title)

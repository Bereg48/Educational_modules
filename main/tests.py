from rest_framework.exceptions import ValidationError
from main.validators import TitleValidator, validator_description_words
from django.test import TestCase
from .serializers import ModuleSerializer
import unittest
from main.models import Module, Section, Payment, Topic
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from django.urls import reverse
import json
from rest_framework.test import APIClient


class ModuleSerializerTests(TestCase):
    """Класс ModuleSerializerTests тестирует функциональности
    ModuleSerializer. Проверяет, что все указанные поля
    `fields` в `ModuleSerializer`, присутствуют в сериализованных
    данных. Также Проверяет, что данные в сериализаторе соответствуют
    данным модуля, который мы создали в `setUp`."""

    def setUp(self):
        self.user = User.objects.create(username='testuser',
                                        password='testpassword')
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
                         set(['id', 'user', 'number',
                              'title', 'description', 'is_paid'])
                         )

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
        self.user = User.objects.create(username='testuser',
                                        password='testpassword')
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

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ModuleSerializer(self.module).data)

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

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'You are not allowed'
                                                  'to view this module '
                                                  'in detail.')

    def test_module_retrieve_unauthenticated(self):
        """
        Test retrieving a module without authentication
        """
        response = self.client.get(f'/module/{self.module.pk}/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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
            user=self.user,
            number=1,
            title='Test Section',
            module=self.module,
            is_paid=True
        )

    def test_section_list_api_view(self):
        url = reverse('main:section-list')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], self.section.title)


class SectionCreateAPIViewTest(APITestCase):
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
        self.section = Section.objects.create(
            user=self.superuser,
            number=1,
            title='New Section',
            module=self.module,
            is_paid=True
        )

    def test_section_create_api_view(self):
        url = '/section/create/'
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(url,
                                    data={'title': 'New Section',
                                          'module': self.module.id,
                                          'number': 1,
                                          'description': 'Section '
                                                         'description',
                                          'user': self.superuser.id}
                                    )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Section.objects.count(), 2)


class SectionUpdateAPIViewTest(APITestCase):
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
        self.section = Section.objects.create(
            user=self.superuser,
            number=1,
            title='New Section',
            module=self.module,
            is_paid=True
        )

    def test_section_update_api_view(self):
        url = f'/section/update/{self.section.id}/'
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        data = {'number': 1, 'user': self.superuser.id,
                'title': 'Updated Title',
                'description': 'Updated Description'}
        response = self.client.put(url, data=json.dumps(data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SectionDestroyAPIViewTest(APITestCase):
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
        self.section = Section.objects.create(
            user=self.superuser,
            number=1,
            title='New Section',
            module=self.module,
            is_paid=True
        )

    def test_section_destroy_api_view(self):
        url = f'/section/delete/{self.section.id}/'
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TopicCreateAPIViewTest(APITestCase):
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
        self.section = Section.objects.create(
            user=self.superuser,
            number=1,
            title='New Section',
            module=self.module,
            is_paid=True
        )
        self.topic = Topic.objects.create(
            user=self.superuser,
            number=1,
            title='New Topic',
            description='Topic 1 description',
            section=self.section
        )

    def test_topic_create_api_view(self):
        url = '/topic/create/'
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        response = self.client.post(url, data={'title': 'New Topic',
                                               'section': self.section.id,
                                               'number': 1,
                                               'description': 'Topic '
                                                              'description',
                                               'user': self.superuser.id})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Topic.objects.count(), 2)


class TopicUpdateAPIViewTest(APITestCase):
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
        self.section = Section.objects.create(
            user=self.superuser,
            number=1,
            title='New Section',
            module=self.module,
            is_paid=True
        )
        self.topic = Topic.objects.create(
            user=self.superuser,
            number=1,
            title='New Topic',
            description='Topic 1 description',
            section=self.section
        )

    def test_topic_update_api_view(self):
        url = f'/topic/update/{self.topic.id}/'
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        data = {'number': 1, 'user': self.superuser.id,
                'title': 'Updated Title',
                'description': 'Updated '
                               'Description'}
        response = self.client.put(url, data=json.dumps(data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TopicDestroyAPIViewTest(APITestCase):
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
        self.section = Section.objects.create(
            user=self.superuser,
            number=1,
            title='New Section',
            module=self.module,
            is_paid=True
        )
        self.topic = Topic.objects.create(
            user=self.superuser,
            number=1,
            title='New Topic',
            description='Topic 1 description',
            section=self.section
        )

    def test_topic_destroy_api_view(self):
        url = f'/topic/delete/{self.topic.id}/'
        self.client = APIClient()
        self.client.force_authenticate(user=self.superuser)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PaymentCreateAPIViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.module = Module.objects.create(
            user=self.user,
            number=1,
            title='Module 1',
            description='Module 1 description',
            is_paid=True
        )
        self.payment_amount = 100

    def test_create_payment(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        url = reverse('main:payment-create',
                      kwargs={'module_id': self.module.id})
        data = {'amount': self.payment_amount}
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {'message': 'Payment successful'})
        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.first()
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.module, self.module)
        self.assertEqual(payment.amount, self.payment_amount)


class TestTitleValidator(unittest.TestCase):
    """Класс TestTitleValidator тестирует функциональность
    класса TitleValidator, который валидирует значение
    поля title, которое должно состоять только из букв,
    цифр и символов: точка, тире и пробел."""

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

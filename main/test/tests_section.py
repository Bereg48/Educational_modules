from main.models import Module, Section
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from django.urls import reverse
import json
from rest_framework.test import APIClient


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
                                          'user': self.superuser.id})

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

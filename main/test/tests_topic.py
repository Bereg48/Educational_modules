from main.models import Module, Section, Topic
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
import json
from rest_framework.test import APIClient


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
                'description': 'Updated Description'}
        response = self.client.put(url,
                                   data=json.dumps(data),
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

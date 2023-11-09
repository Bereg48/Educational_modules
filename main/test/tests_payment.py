from django.test import TestCase
from main.models import Module, Payment
from rest_framework import status
from users.models import User
from django.urls import reverse
from rest_framework.test import APIClient


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

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)
        self.assertEqual(response.data,
                         {'message': 'Payment successful'})
        self.assertEqual(Payment.objects.count(), 1)
        payment = Payment.objects.first()
        self.assertEqual(payment.user, self.user)
        self.assertEqual(payment.module, self.module)
        self.assertEqual(payment.amount, self.payment_amount)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Module, Payment
from main.serializers import PaymentSerializer


class PaymentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]  # требуется аутентификация пользователя
    serializer_class = PaymentSerializer

    def post(self, request, module_id):
        """Метод post обрабатывает POST-запросы для создания нового платежа.
        Принимает два аргумента: `request` - объект запроса
        и `module_id` - идентификатор модуля, для которого будет создан платеж.
        Сначала мы получаем объект модуля с помощью Module.objects.get(id=module_id),
        используя переданный в запросе идентификатор module_id. Затем получаем
        текущего пользователя через request.user. Далее, создаем новый объект `Payment`,
        указывая пользователя (`user`), модуль (`module`) и сумму платежа (`payment_amount`).
        После сохранения объекта `Payment` в базу данных с помощью `payment.save()`,
        возвращается ответ `Response` с сообщением 'Payment successful'.
        Это означает, что платеж успешно создан."""
        module = Module.objects.get(id=module_id)
        user = request.user
        payment_amount = 100  # Пример суммы платежа
        payment = Payment(user=user, module=module, amount=payment_amount)
        payment.save()
        return Response({'message': 'Payment successful'})

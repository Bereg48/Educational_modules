from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from main.models import Module, Payment
from main.serializers import PaymentSerializer


class PaymentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]  # требуется аутентификация пользователя
    serializer_class = PaymentSerializer

    def create(self, request, *args, **kwargs):
        """метод `create` переопределен, чтобы обработать POST-запросы.
        Он принимает аргументы `request`, `*args` и `**kwargs`. `request`
        содержит информацию о запросе. `*args` и `**kwargs` позволяют
        передавать дополнительные аргументы не известные заранее."""
        module_id = kwargs.get('module_id')
        module = Module.objects.get(id=module_id)
        user = request.user
        payment_amount = 100  # Пример суммы платежа
        payment = Payment(user=user, module=module, amount=payment_amount)
        payment.save()
        return Response({'message': 'Payment successful'}, status=status.HTTP_201_CREATED)

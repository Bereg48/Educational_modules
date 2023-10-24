from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from .models import Module, Section, Topic, Payment
from .serializers import ModuleSerializer, SectionSerializer, TopicSerializer, PaymentSerializer


class ModuleListAPIView(generics.ListAPIView):
    """Класс ModuleListAPIView отвечает за функциональность просмотра при применении
        класса ModuleSerializer, который функционирует в соответствии с определенной моделью класса Module"""
    queryset = Module.objects.all().order_by('id')
    serializer_class = ModuleSerializer


class ModuleCreateAPIView(generics.CreateAPIView):
    """Класс ModuleCreateAPIView отвечает за функциональность создания при применении
        класса ModuleSerializer, который функционирует в соответствии с определенной моделью класса Module"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ModuleRetrieveAPIView(generics.RetrieveAPIView):
    """Класс ModuleRetrieveAPIView отвечает за функциональность просмотра конкректного модуля при применении
            класса ModuleSerializer, который функционирует в соответствии с определенной моделью класса Module"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_queryset(self):
        return Module.objects.all()

    def get_object(self):
        module = super().get_object()
        user = self.request.user
        if not module.is_paid_by(user):  # Проверяем, оплатил ли пользователь модуль
            raise PermissionDenied('You are not allowed to view this module in detail.')  # Вызываем исключение, если модуль не оплачен
        return module


class ModuleUpdateAPIView(generics.UpdateAPIView):
    """Класс ModuleUpdateAPIView отвечает за функциональность обновления конкректного модуля при применении
            класса ModuleSerializer, который функционирует в соответствии с определенной моделью класса Module"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Module.objects.filter(user=self.request.user)


class ModuleDestroyAPIView(generics.DestroyAPIView):
    """Класс ModuleDestroyAPIView отвечает за функциональность удаления конкретного объекта при применении
            класса ModuleSerializer, который функционирует в соответствии с определенной моделью класса Module"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Module.objects.filter(user=self.request.user)


############################################################################


class SectionListAPIView(generics.ListAPIView):
    """Класс SectionListAPIView отвечает за функциональность просмотра при применении
        класса SectionSerializer, который функционирует в соответствии с определенной моделью класса Section"""
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем список разделов, доступных пользователю
        user = self.request.user
        sections = Section.objects.all().order_by('id')

        # Фильтруем только оплаченные разделы
        paid_sections = [section for section in sections if section.module.is_paid]

        return paid_sections


class SectionCreateAPIView(generics.CreateAPIView):
    """Класс SectionCreateAPIView отвечает за функциональность создания при применении
        класса SectionSerializer, который функционирует в соответствии с определенной моделью класса Section"""
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SectionRetrieveAPIView(generics.RetrieveAPIView):
    """Класс SectionRetrieveAPIView отвечает за функциональность просмотра конкректного модуля при применении
            класса SectionSerializer, который функционирует в соответствии с определенной моделью класса Section"""
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        sections = Section.objects.all()

        # Фильтруем только оплаченные разделы
        paid_sections = [section for section in sections if section.module.is_paid]

        return paid_sections


class SectionUpdateAPIView(generics.UpdateAPIView):
    """Класс SectionUpdateAPIView отвечает за функциональность обновления конкректного модуля при применении
            класса SectionSerializer, который функционирует в соответствии с определенной моделью класса Section"""
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Section.objects.filter(user=self.request.user)


class SectionDestroyAPIView(generics.DestroyAPIView):
    """Класс SectionDestroyAPIView отвечает за функциональность удаления конкретного объекта при применении
            класса SectionSerializer, который функционирует в соответствии с определенной моделью класса Section"""
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Section.objects.filter(user=self.request.user)


############################################################################


class TopicListAPIView(generics.ListAPIView):
    """Класс TopicListAPIView отвечает за функциональность просмотра при применении
        класса TopicSerializer, который функционирует в соответствии с определенной моделью класса Topic"""
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Получаем список тем, доступных пользователю
        user = self.request.user
        topics = Topic.objects.all().order_by('id')

        # Фильтруем только оплаченные темы
        paid_topics = [topic for topic in topics if topic.section.module.is_paid]
        return paid_topics


class TopicCreateAPIView(generics.CreateAPIView):
    """Класс TopicCreateAPIView отвечает за функциональность создания при применении
        класса TopicSerializer, который функционирует в соответствии с определенной моделью класса Topic"""
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TopicRetrieveAPIView(generics.RetrieveAPIView):
    """Класс TopicRetrieveAPIView отвечает за функциональность просмотра конкректного модуля при применении
            класса TopicSerializer, который функционирует в соответствии с определенной моделью класса Topic"""
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        topics = Topic.objects.all()

        # Фильтруем только оплаченные темы
        paid_topics = [topic for topic in topics if topic.section.module.is_paid]

        return paid_topics


class TopicUpdateAPIView(generics.UpdateAPIView):
    """Класс TopicUpdateAPIView отвечает за функциональность обновления конкректного модуля при применении
            класса TopicSerializer, который функционирует в соответствии с определенной моделью класса Topic"""
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user)


class TopicDestroyAPIView(generics.DestroyAPIView):
    """Класс TopicDestroyAPIView отвечает за функциональность удаления конкретного объекта при применении
            класса TopicSerializer, который функционирует в соответствии с определенной моделью класса Topic"""
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Topic.objects.filter(user=self.request.user)


class PaymentCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]  # требуется аутентификация пользователя
    serializer_class = PaymentSerializer

    def post(self, request, module_id):
        module = Module.objects.get(id=module_id)
        user = request.user
        payment_amount = 100  # Пример суммы платежа
        payment = Payment(user=user, module=module, amount=payment_amount)
        payment.save()
        return Response({'message': 'Payment successful'})

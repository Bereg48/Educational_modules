from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated

from main.models import Module
from main.serializers import ModuleSerializer


class ModuleListAPIView(generics.ListAPIView):
    """Класс ModuleListAPIView отвечает за функциональность просмотра
    при применении класса ModuleSerializer, который функционирует
    в соответствии с определенной моделью класса Module"""
    queryset = Module.objects.all().order_by('id')
    serializer_class = ModuleSerializer
    permission_classes = [IsAuthenticated]


class ModuleCreateAPIView(generics.CreateAPIView):
    """Класс ModuleCreateAPIView отвечает за функциональность создания
    при применении класса ModuleSerializer, который функционирует
    в соответствии с определенной моделью класса Module"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        """Метод perform_create вызывается при создании нового объекта модуля
        и сохраняет пользователя (self.request.user) в поле user сериализатора."""
        serializer.save(user=self.request.user)


class ModuleRetrieveAPIView(generics.RetrieveAPIView):
    """Класс ModuleRetrieveAPIView отвечает за функциональность просмотра
    конкректного модуля при применении класса ModuleSerializer, который
    функционирует в соответствии с определенной моделью класса Module"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def get_object(self):
        """Метод get_object вызывается для получения конкретного объекта модуля,
        который будет просмотрен. В этом методе выполняется проверка, оплачен ли
        модуль пользователем (module.is_paid_by(user)). Если модуль не был оплачен,
        вызывается исключение PermissionDenied с соответствующим сообщением.
        Если модуль оплачен, возвращается объект модуля"""
        module = super().get_object()
        user = self.request.user
        if not module.is_paid_by(user):  # Проверяем, оплатил ли пользователь модуль
            raise PermissionDenied(
                'You are not allowed'
                'to view this module in detail.')  # Вызываем исключение, если модуль не оплачен
        return module


class ModuleUpdateAPIView(generics.UpdateAPIView):
    """Класс ModuleUpdateAPIView отвечает за функциональность обновления
    конкректного модуля при применении класса ModuleSerializer, который
    функционирует в соответствии с определенной моделью класса Module"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """Метод get_queryset возвращает запрос, который получает все объекты
        модели Module, отфильтрованные по полю user, который соответствует
        текущему пользователю (self.request.user)."""
        return Module.objects.filter(user=self.request.user)


class ModuleDestroyAPIView(generics.DestroyAPIView):
    """Класс ModuleDestroyAPIView отвечает за функциональность удаления
    конкретного объекта при применении класса ModuleSerializer, который
    функционирует в соответствии с определенной моделью класса Module"""
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """Метод get_queryset возвращает запрос, который получает
        все объекты модели Module, отфильтрованные по полю user,
        который соответствует текущему пользователю (self.request.user)."""
        return Module.objects.filter(user=self.request.user)

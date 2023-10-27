from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from main.models import Section
from main.serializers import SectionSerializer


class SectionListAPIView(generics.ListAPIView):
    """Класс SectionListAPIView отвечает за функциональность
    просмотра при применении класса SectionSerializer, который
    функционирует в соответствии с определенной моделью класса Section"""
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Метод get_queryset определяет начальный набор данных,
        который будут использоваться при выполнении запроса.
        В данном случае, возвращается список разделов, доступных
        пользователю. Сначала получаем текущего пользователя
        через `self.request.user`. Затем получаем все разделы,
        используя Section.objects.all(), отсортированные
        по полю 'id'. Далее фильтруется только те разделы, которые
        являются платными. Это делается с помощью проверки каждого
        раздела, если его связанный модуль (`module`) имеет
        признак оплаты (`is_paid`), то такой раздел считается
        оплаченным и добавляется в список paid_sections."""
        # Получаем список разделов, доступных пользователю
        sections = Section.objects.all().order_by('id')

        # Фильтруем только оплаченные разделы
        paid_sections = [section for section in sections if section.module.is_paid]

        return paid_sections


class SectionCreateAPIView(generics.CreateAPIView):
    """Класс SectionCreateAPIView отвечает за функциональность
    создания при применении класса SectionSerializer, который
    функционирует в соответствии с определенной моделью класса Section"""
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        """Метод perform_create вызывается при создании нового объекта модуля
        и сохраняет пользователя (self.request.user) в поле user сериализатора."""
        serializer.save(user=self.request.user)


class SectionRetrieveAPIView(generics.RetrieveAPIView):
    """Класс SectionRetrieveAPIView отвечает за функциональность
    просмотра конкректного модуля при применении класса SectionSerializer,
    который функционирует в соответствии с определенной моделью класса Section"""
    serializer_class = SectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Метод get_queryset определяет начальный набор данных, который будут
        использоваться при выполнении запроса. В данном случае, возвращается список
        разделов, доступных пользователю. Сначала получаем текущего пользователя
        через `self.request.user`. Затем получаем все разделы,
        используя Section.objects.all(), отсортированные по полю 'id'.
        Далее фильтруется только те разделы, которые являются платными.
        Это делается с помощью проверки каждого раздела, если
        его связанный модуль (`module`) имеет признак оплаты (`is_paid`),
        то такой раздел считается оплаченным и добавляется в список paid_sections."""
        sections = Section.objects.all()

        # Фильтруем только оплаченные разделы
        paid_sections = [section for section in sections if section.module.is_paid]

        return paid_sections


class SectionUpdateAPIView(generics.UpdateAPIView):
    """Класс SectionUpdateAPIView отвечает за функциональность обновления
    конкректного модуля при применении класса SectionSerializer, который
    функционирует в соответствии с определенной моделью класса Section"""
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """Метод get_queryset возвращает запрос, который получает все объекты
        модели Module, отфильтрованные по полю user, которые соответствует
        текущему пользователю (self.request.user)."""
        return Section.objects.filter(user=self.request.user)


class SectionDestroyAPIView(generics.DestroyAPIView):
    """Класс SectionDestroyAPIView отвечает за функциональность удаления конкретного
    объекта при применении класса SectionSerializer, который функционирует
    в соответствии с определенной моделью класса Section"""
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """Метод get_queryset возвращает запрос, который получает
        все объекты модели Module, отфильтрованные по полю user,
        которые соответствует текущему пользователю (self.request.user)."""
        return Section.objects.filter(user=self.request.user)

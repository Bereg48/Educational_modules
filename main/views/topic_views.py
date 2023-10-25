from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from main.models import Topic
from main.serializers import TopicSerializer


class TopicListAPIView(generics.ListAPIView):
    """Класс TopicListAPIView отвечает за функциональность просмотра при применении
        класса TopicSerializer, который функционирует в соответствии с определенной моделью класса Topic"""
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Метод get_queryset определяет начальный набор данных, который будет использоваться при выполнении запроса.
        В данном случае, возвращается список тем, доступных пользователю. Сначала получаем текущего пользователя
        через `self.request.user`. Затем получаем все темы, используя `Topic.objects.all()`, отсортированные по полю 'id'.
        Затем фильтруется список тем, оставляя только те, которые относятся к разделам с оплатой.
        Это делается с помощью проверки каждой темы. Если связанный с темой раздел (`section`) имеет
        признак оплаты ('is_paid'), то такая тема добавляется в список paid_topics. Наконец, метод get_queryset
        возвращает список paid_topics, который будет использоваться для вывода списка тем в представлении."""
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
        """Метод perform_create вызывается при создании нового объекта модуля
        и сохраняет пользователя (self.request.user) в поле user сериализатора."""
        serializer.save(user=self.request.user)


class TopicRetrieveAPIView(generics.RetrieveAPIView):
    """Класс TopicRetrieveAPIView отвечает за функциональность просмотра конкректного модуля при применении
            класса TopicSerializer, который функционирует в соответствии с определенной моделью класса Topic"""
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Метод get_queryset определяет начальный набор данных, который будет использоваться при выполнении запроса.
        В данном случае, возвращается список тем, доступных пользователю. Сначала получаем текущего пользователя
        через `self.request.user`. Затем получаем все темы, используя `Topic.objects.all()`, отсортированные по полю 'id'.
        Затем фильтруется список тем, оставляя только те, которые относятся к разделам с оплатой.
        Это делается с помощью проверки каждой темы. Если связанный с темой раздел (`section`) имеет
        признак оплаты ('is_paid'), то такая тема добавляется в список paid_topics. Наконец, метод get_queryset
        возвращает список paid_topics, который будет использоваться для вывода списка тем в представлении."""
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
        """Метод get_queryset возвращает запрос, который получает все объекты модели Module, отфильтрованные
        по полю user, которые соответствует текущему пользователю (self.request.user)."""
        return Topic.objects.filter(user=self.request.user)


class TopicDestroyAPIView(generics.DestroyAPIView):
    """Класс TopicDestroyAPIView отвечает за функциональность удаления конкретного объекта при применении
            класса TopicSerializer, который функционирует в соответствии с определенной моделью класса Topic"""
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """Метод get_queryset возвращает запрос, который получает все объекты модели Module, отфильтрованные
        по полю user, которые соответствует текущему пользователю (self.request.user)."""
        return Topic.objects.filter(user=self.request.user)
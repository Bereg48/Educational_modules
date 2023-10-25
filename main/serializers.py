from rest_framework import serializers
from .models import Module, Section, Topic, Payment


class ModuleSerializer(serializers.ModelSerializer):
    """Класс ModuleSerializer сериализует данные полученные в соответствии с установленной моделью класса Module,
    данные сериализуются, в рамках функциональности CRUD"""

    class Meta:
        model = Module
        fields = '__all__'


class SectionSerializer(serializers.ModelSerializer):
    """Класс SectionSerializer сериализует данные полученные в соответствии с установленной моделью класса Section,
    данные сериализуются, в рамках функциональности CRUD"""

    class Meta:
        model = Section
        fields = '__all__'


class TopicSerializer(serializers.ModelSerializer):
    """Класс TopicSerializer сериализует данные полученные в соответствии с установленной моделью класса Topic,
    данные сериализуются, в рамках функциональности CRUD"""

    class Meta:
        model = Topic
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

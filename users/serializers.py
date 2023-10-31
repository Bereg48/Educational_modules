from rest_framework import serializers
from users.models import User


class UserSerializers(serializers.ModelSerializer):
    """Класс UserSerializers сериализует данные полученные
    в соответствии с установленной моделью класса User,
    данные сериализуются, в рамках функциональности CRUD"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        groups_data = validated_data.pop('groups', [])
        permissions_data = validated_data.pop('user_permissions', [])

        instance = User.objects.create_user(**validated_data)

        if password is not None:
            instance.set_password(password)

        instance.save()

        for group in groups_data:
            instance.groups.add(group)

        for permission in permissions_data:
            instance.user_permissions.add(permission)

        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

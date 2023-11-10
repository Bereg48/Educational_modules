from rest_framework import generics, permissions

from main.models import UserModuleProgress
from main.serializers import UserModuleProgressSerializer


class CreateUserModuleProgressView(generics.CreateAPIView):
    queryset = UserModuleProgress.objects.all()
    serializer_class = UserModuleProgressSerializer
    permission_classes = [permissions.IsAdminUser]


class ListUserModuleProgressView(generics.ListAPIView):
    queryset = UserModuleProgress.objects.all()
    serializer_class = UserModuleProgressSerializer
    permission_classes = [permissions.IsAdminUser]


class RetrieveUserModuleProgressView(generics.RetrieveAPIView):
    queryset = UserModuleProgress.objects.all()
    serializer_class = UserModuleProgressSerializer
    permission_classes = [permissions.IsAdminUser]


class UpdateUserModuleProgressView(generics.UpdateAPIView):
    queryset = UserModuleProgress.objects.all()
    serializer_class = UserModuleProgressSerializer

    def perform_update(self, serializer):
        user = self.request.user
        module = self.get_object().module
        progress = self.request.data.get('progress')
        serializer.save(user=user, module=module, progress=progress)


class DeleteUserModuleProgressView(generics.DestroyAPIView):
    queryset = UserModuleProgress.objects.all()
    serializer_class = UserModuleProgressSerializer
    permission_classes = [permissions.IsAdminUser]

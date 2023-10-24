from django.urls import path

from .apps import MainConfig
from .views import *

app_name = MainConfig.name

urlpatterns = [
    path('module/', ModuleListAPIView.as_view(), name='module-list'),
    path('module/create/', ModuleCreateAPIView.as_view(), name='module-create'),
    path('module/<int:pk>/', ModuleRetrieveAPIView.as_view(), name='module-retrieve'),
    path('module/update/<int:pk>/', ModuleUpdateAPIView.as_view(), name='module-update'),
    path('module/delete/<int:pk>/', ModuleDestroyAPIView.as_view(), name='module-destroy'),
    path('section/', SectionListAPIView.as_view(), name='section-list'),
    path('section/create/', SectionCreateAPIView.as_view(), name='section-create'),
    path('section/<int:pk>/', SectionRetrieveAPIView.as_view(), name='section-retrieve'),
    path('section/update/<int:pk>/', SectionUpdateAPIView.as_view(), name='section-update'),
    path('section/delete/<int:pk>/', SectionDestroyAPIView.as_view(), name='section-destroy'),
    path('topic/', TopicListAPIView.as_view(), name='topic-list'),
    path('topic/create/', TopicCreateAPIView.as_view(), name='topic-create'),
    path('topic/<int:pk>/', TopicRetrieveAPIView.as_view(), name='topic-retrieve'),
    path('topic/update/<int:pk>/', TopicUpdateAPIView.as_view(), name='topic-update'),
    path('topic/delete/<int:pk>/', TopicDestroyAPIView.as_view(), name='topic-destroy'),

]

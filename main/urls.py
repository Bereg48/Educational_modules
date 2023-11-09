from django.urls import path

from .apps import MainConfig
from main.views.module_views import ModuleListAPIView, \
    ModuleCreateAPIView, ModuleRetrieveAPIView, \
    ModuleUpdateAPIView, ModuleDestroyAPIView
from main.views.payment_views import PaymentCreateAPIView
from main.views.section_views import SectionListAPIView, \
    SectionCreateAPIView, \
    SectionRetrieveAPIView, SectionUpdateAPIView, \
    SectionDestroyAPIView
from main.views.topic_views import TopicListAPIView, \
    TopicCreateAPIView, TopicRetrieveAPIView, TopicUpdateAPIView, \
    TopicDestroyAPIView
from .views.user_module_progress_views import ListUserModuleProgressView, CreateUserModuleProgressView, \
    RetrieveUserModuleProgressView, UpdateUserModuleProgressView, DeleteUserModuleProgressView

app_name = MainConfig.name

urlpatterns = [
    path('module/',
         ModuleListAPIView.as_view(), name='module-list'),
    path('module/create/',
         ModuleCreateAPIView.as_view(), name='module-create'),
    path('module/<int:pk>/',
         ModuleRetrieveAPIView.as_view(), name='module-retrieve'),
    path('module/update/<int:pk>/',
         ModuleUpdateAPIView.as_view(), name='module-update'),
    path('module/delete/<int:pk>/',
         ModuleDestroyAPIView.as_view(), name='module-destroy'),
    path('section/',
         SectionListAPIView.as_view(), name='section-list'),
    path('section/create/',
         SectionCreateAPIView.as_view(), name='section-create'),
    path('section/<int:pk>/',
         SectionRetrieveAPIView.as_view(), name='section-retrieve'),
    path('section/update/<int:pk>/',
         SectionUpdateAPIView.as_view(), name='section-update'),
    path('section/delete/<int:pk>/',
         SectionDestroyAPIView.as_view(), name='section-destroy'),
    path('topic/',
         TopicListAPIView.as_view(), name='topic-list'),
    path('topic/create/',
         TopicCreateAPIView.as_view(), name='topic-create'),
    path('topic/<int:pk>/',
         TopicRetrieveAPIView.as_view(), name='topic-retrieve'),
    path('topic/update/<int:pk>/',
         TopicUpdateAPIView.as_view(), name='topic-update'),
    path('topic/delete/<int:pk>/',
         TopicDestroyAPIView.as_view(), name='topic-destroy'),
    path('payment/create/<int:module_id>/',
         PaymentCreateAPIView.as_view(), name='payment-create'),
    path('progress/',
         ListUserModuleProgressView.as_view(), name='progress-list'),
    path('progress/create/',
         CreateUserModuleProgressView.as_view(), name='progress-create'),
    path('progress/<int:pk>/',
         RetrieveUserModuleProgressView.as_view(), name='topic-retrieve'),
    path('progress/update/<int:pk>/',
         UpdateUserModuleProgressView.as_view(), name='progress-update'),
    path('progress/delete/<int:pk>/',
         DeleteUserModuleProgressView.as_view(), name='topic-destroy'),

]

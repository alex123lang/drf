from django.urls import path

from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonListAPIView, LessonRetrieveAPIView, LessonCreateAPIView, \
        LessonDestroyAPIView, LessonUpdateAPIView, SubscriptionCreateAPIView

router = DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

app_name = MaterialsConfig.name


urlpatterns = [
        path('lessons/', LessonListAPIView.as_view(), name='lessons-list'),
        path('lessons/create/', LessonCreateAPIView.as_view(), name='lessons-create'),
        path('lessons/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lessons-retrieve'),
        path('lessons/<int:pk>/update/', LessonUpdateAPIView.as_view(), name='lessons-update'),
        path('lessons/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name='lessons-delete'),
        path('subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription-create')
] + router.urls

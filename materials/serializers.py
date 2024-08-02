from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import YoutubeLinkValidator


class LessonSerializer(ModelSerializer):
    validators = [YoutubeLinkValidator(field='link_to_video')]

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(ModelSerializer):
    count_lesson_in_course = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_count_lesson_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_is_subscribed(self, course):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user, course=course
            ).exists()
        return False

    class Meta:
        model = Course
        fields = ('name', 'description', 'image', 'count_lesson_in_course', 'lessons', 'is_subscribed')


class SubscriptionSerializer(ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'

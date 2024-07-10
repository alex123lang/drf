from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(ModelSerializer):
    lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'


class CourseDetailSerializer(ModelSerializer):
    count_lesson_in_course = SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)

    def get_lessons(self, course):
        return [(lesson.name, lesson.description, lesson.image) for lesson in Lesson.objects.filter(course=course)]

    def get_count_lesson_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    class Meta:
        model = Course
        fields = ('name', 'description', 'image', 'count_lesson_in_course',)


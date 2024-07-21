from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin1@localhost')
        self.course = Course.objects.create(name='Програмного обеспечения')
        self.lesson = Lesson.objects.create(name='Основы программирования', author=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        self.url = reverse('materials:lessons-retrieve', args=(self.lesson.pk,))
        self.data = {
            'name': 'Основы программирования',
        }
        response = self.client.get(self.url)
        self. data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)

    def test_lesson_create(self):
        self.url = reverse('materials:lessons-create')
        self.data = {
            "name": "Основы backend-разработки",
            "description": "Внутренняя часть цифрового продукта",
        }
        response = self.client.post(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['name'], "Основы backend-разработки")
        self.assertEqual(
            Lesson.objects.all().count(), 2)

    def test_lesson_update(self):
        self.url = reverse('materials:lessons-update', args=(self.lesson.pk,))
        self.data = {
            "name": "Основы backend-разработки",
            "description": "Внутренняя часть цифрового продукта",
        }
        response = self.client.put(self.url, self.data)
        self.data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Основы backend-разработки")

    def test_lesson_delete(self):
        self.url = reverse('materials:lessons-delete', args=(self.lesson.pk,))
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            Lesson.objects.all().count(), 0)


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='admin1@localhost')
        self.course = Course.objects.create(name='Програмное обеспечение')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('materials:subscription-create')

    def test_subscription_activate(self):
        """Тест подписки на курс"""
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                "message": "Подписка добавлена",
            },
        )
        self.assertTrue(
            Subscription.objects.all().exists(),
        )

    def test_sub_deactivate(self):
        """Тест отписки с курса"""
        Subscription.objects.create(user=self.user, course=self.course)
        data = {
            "user": self.user.id,
            "course": self.course.id,
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.json(),
            {
                "message": "Подписка удалена",
            },
        )
        self.assertFalse(
            Subscription.objects.all().exists(),
        )

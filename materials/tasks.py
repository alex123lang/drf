from celery import shared_task
from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription


@shared_task
def sending_emails_for_update_course(course_id):
    course_subscriptions = Subscription.objects.filter(course=course_id)
    for subscription in course_subscriptions:
        send_mail(
            subject="Обновление материалов курса",
            message=f'Курс {subscription.course.name} был обновлен.',
            from_email=EMAIL_HOST_USER,
            recipient_list=[subscription.user.email],
            fail_silently=False
        )

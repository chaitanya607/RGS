from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django_celery_beat.models import PeriodicTask
from .models import Emails

from django_celery_beat.models import CrontabSchedule


@receiver(post_save, sender=Emails)
def schedule_email(sender, instance, created, **kwargs):
    for day in instance.repeat_days.all():
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute=instance.run_time.minute,
            hour=instance.run_time.hour,
            day_of_week=str(day.day),  # 0 for Monday, 1 for Tuesday, etc.
        )

        task_name = f"send-email-{instance.id}-day-{day.day}"

        PeriodicTask.objects.update_or_create(
            name=task_name,
            defaults={
                'crontab': schedule,
                'task': 'core.tasks.send_scheduled_email',
                'args': [instance.id],
            }
        )


@receiver(post_delete, sender=Emails)
def unschedule_email(sender, instance, **kwargs):
    # Remove the periodic task
    task_name = f"send-email-{instance.id}"
    try:
        task = PeriodicTask.objects.get(name=task_name)
        task.delete()
    except PeriodicTask.DoesNotExist:
        pass

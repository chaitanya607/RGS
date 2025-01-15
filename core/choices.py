from django.db import models
from django.utils.translation import gettext as _


class FileExtensionChoices(models.TextChoices):
    EXCEL = "excel"
    CSV = "csv"
    PDF = "pdf"


class StatusChoices(models.TextChoices):
    ONGOING = "ongoing"
    COMPLETED = "completed"
    FAILED = "failed"
    SCHEDULED = "scheduled"


class DayOfWeekChoices(models.IntegerChoices):
    MONDAY = 0, _('Monday')
    TUESDAY = 1, _('Tuesday')
    WEDNESDAY = 2, _('Wednesday')
    THURSDAY = 3, _('Thursday')
    FRIDAY = 4, _('Friday')
    SATURDAY = 5, _('Saturday')
    SUNDAY = 6, _('Sunday')


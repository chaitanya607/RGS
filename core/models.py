import calendar
import os

from django.db import models
from django.conf import settings

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
from .choices import FileExtensionChoices, StatusChoices, DayOfWeekChoices

from tinymce import models as tinymce_models


class BaseModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    class Meta(object):
        abstract = True  # this is an abstract model

    def is_deleted(self, *args, **kwargs):
        return self.deleted is not None


class TimeStampedModel(BaseModel):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta(object):
        abstract = True


class EmailTemplate(BaseModel):
    name = models.CharField(max_length=255, unique=True, help_text="Unique name for the template file.")
    content = tinymce_models.HTMLField(help_text="Enter the HTML content or plain text for the email template.")

    def save_template_to_file(self):
        # Define the file path to save the template
        template_dir = os.path.join(settings.BASE_DIR, 'templates', 'email_templates')
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)

        # The file name will be based on the template name with .html extension
        file_name = f"{self.name}.html"
        file_path = os.path.join(template_dir, file_name)

        # Save the content to the file
        with open(file_path, 'w') as file:
            file.write(self.content)

    def save(self, *args, **kwargs):
        # Call the parent save method to save the object to the database
        super().save(*args, **kwargs)

        # Save the content to the actual file in the templates directory
        self.save_template_to_file()

    def __str__(self):
        return self.name


class WeekDays(BaseModel):
    day = models.IntegerField(choices=DayOfWeekChoices.choices, null=True, blank=True, unique=True)

    def __str__(self):
        weekdays = list(calendar.day_name)
        # Return the corresponding weekday name
        return weekdays[self.day]

    class Meta:
        verbose_name_plural = "Days of Week"


class Media(SafeDeleteModel):
    FILE = 'file'
    ATTACHMENT = 'attachment'

    MEDIA_TYPE_CHOICES = [
        (FILE, 'File'),
        (ATTACHMENT, 'Attachment'),
    ]

    file = models.FileField(upload_to="media/files")
    extension = models.CharField(choices=FileExtensionChoices.choices, default=FileExtensionChoices.EXCEL, max_length=100)
    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    object_id = models.IntegerField(null=True, blank=True)
    content_object = GenericForeignKey()

    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES, default=FILE)

    def __str__(self):
        return f"{self.media_type}: {self.file.name}"


class Emails(TimeStampedModel):
    repeat_days = models.ManyToManyField(WeekDays)
    run_time = models.TimeField(null=True)
    subject = models.CharField(max_length=1000, null=False, default="")
    template = models.ForeignKey(EmailTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(choices=StatusChoices.choices, default=StatusChoices.SCHEDULED, max_length=100)
    file = GenericRelation(Media)
    attachments = GenericRelation(Media)

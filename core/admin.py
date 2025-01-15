from django.contrib import admin
from safedelete.admin import SafeDeleteAdmin, highlight_deleted
from django.contrib.contenttypes.admin import GenericTabularInline

from utilities.datetime_filters import date_filters
from .forms import AttachmentForm, EmailsAdminForm
from .models import Emails, Media, WeekDays, EmailTemplate
from .choices import StatusChoices


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    fields = ['name', 'content']
    save_on_top = True


class FileInline(GenericTabularInline):
    model = Media
    ct_field = "content_type"
    ct_fk_field = "object_id"
    extra = 1
    verbose_name = "File"
    verbose_name_plural = "Files"

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(media_type=Media.FILE)

    def save_model(self, request, obj, form, change):
        obj.media_type = Media.FILE  # Ensure this is saved as a file
        super().save_model(request, obj, form, change)


class AttachmentsInline(GenericTabularInline):
    model = Media
    ct_field = "content_type"
    ct_fk_field = "object_id"
    extra = 1
    verbose_name = "Attachment"
    verbose_name_plural = "Attachments"
    form = AttachmentForm

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(media_type=Media.ATTACHMENT)

    def save_model(self, request, obj, form, change):
        obj.media_type = Media.ATTACHMENT  # Ensure this is saved as an attachment
        super().save_model(request, obj, form, change)


@admin.register(Emails)
class EmailsAdmin(SafeDeleteAdmin):
    form = EmailsAdminForm
    list_display = (highlight_deleted, "status")
    list_per_page = 25
    list_filter = date_filters + SafeDeleteAdmin.list_filter + ("status", )
    actions = ["mark_as_completed", "mark_as_ongoing", "mark_as_failed", "mark_as_scheduled"]
    inlines = [FileInline, AttachmentsInline]

    # Use autocomplete_fields for the template selection
    autocomplete_fields = ['template']
    fields = ('subject', 'template', 'repeat_days', 'run_time', 'status')

    def get_queryset(self, request):
        # Allow admin to search templates
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('template')  # Prefetch related for efficiency
        return queryset

    class Media:
        js = ('js/admin_template_preview.js',)

        # Optionally, you can load some admin CSS for further styling
        css = {
            'all': ('css/admin_custom.css',)
        }

    def mark_as_completed(self, request, queryset):
        queryset.update(status=StatusChoices.COMPLETED)

    mark_as_completed.short_description = "Mark selected Emails as completed"

    def mark_as_ongoing(self, request, queryset):
        queryset.update(status=StatusChoices.ONGOING)

    mark_as_ongoing.short_description = "Mark selected Emails as ongoing"

    def mark_as_failed(self, request, queryset):
        queryset.update(status=StatusChoices.FAILED)

    mark_as_failed.short_description = "Mark selected Emails as failed"

    def mark_as_scheduled(self, request, queryset):
        queryset.update(status=StatusChoices.SCHEDULED)

    mark_as_scheduled.short_description = "Mark selected Emails as scheduled"


@admin.register(WeekDays)
class WeekDaysAdmin(SafeDeleteAdmin):
    list_display = (highlight_deleted, )
    list_per_page = 25


@admin.register(Media)
class MediaAdmin(SafeDeleteAdmin):
    list_display = (highlight_deleted, )
    list_per_page = 25

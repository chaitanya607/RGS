from .models import Media, EmailTemplate

from django import forms
from .models import Emails


class EmailsAdminForm(forms.ModelForm):
    class Meta:
        model = Emails
        fields = ['subject', 'template', 'repeat_days', 'run_time', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # Only if editing an existing email
            for template in EmailTemplate.objects.all():
                self.fields['template'].widget.choices.queryset = EmailTemplate.objects.all()
                self.fields['template'].widget.attrs['data-content'] = template.content

    def as_p(self):
        original_output = super().as_p()
        preview_html = '<div id="template-preview" style="border: 1px solid #ccc; padding: 10px; margin-top: 10px;">Template preview will appear here.</div>'
        return original_output + preview_html


class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Media
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Prepopulate the media_type as 'attachment'
        self.fields['media_type'].initial = Media.ATTACHMENT

import os
import pandas as pd
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from celery import shared_task
from .models import Emails, Media


@shared_task
def send_scheduled_email(email_id):
    try:
        # Get the email object based on the provided email_id
        email_obj = Emails.objects.get(id=email_id)
    except Emails.DoesNotExist:
        print(f"Email with id {email_id} does not exist.")
        return

    # Default subject from the email object
    default_subject = email_obj.subject

    # Get all the media files that are marked as 'file'
    media_files = email_obj.file.all()
    attachments = email_obj.attachments.all()

    # Loop over each media file and load the email addresses and additional data (Excel file)
    for media in media_files:
        if media.extension == 'xlsx':  # Assuming 'xlsx' is the extension for Excel files
            file_path = media.file.path  # Path to the Excel file

            # Load the Excel file using pandas to extract email addresses, recipient name, and subject (optional)
            try:
                df = pd.read_excel(file_path)
                email_addresses = df['email'].tolist()  # Assuming there's a column named 'email'
                recipient_names = df.get('recipient_name', [''] * len(email_addresses))  # Optional, defaults to empty
                subjects = df.get('subject',  default_subject)  # Optional, defaults to email_obj.subject
            except Exception as e:
                print(f"Error reading Excel file: {e}")
                continue  # Skip if there's an error

            # Prepare the email object
            for i, email_address in enumerate(email_addresses):
                recipient_name = recipient_names[i]
                subject = subjects[i]

                # Prepare the email content using Django's template rendering
                context = {
                    'subject': subject,  # Using either the Excel-provided or default subject
                    'body': 'This is your email body',  # Replace with actual body if needed
                    'recipient_name': recipient_name,  # Add recipient name to context
                    # Add other context data here if needed
                }

                # Render the template with the context
                template_name = email_obj.template.name  # This gives you the template name
                email_content = render_to_string(f"email_templates/{template_name}.html", context)

                # Create the email message
                email_msg = EmailMessage(
                    subject=subject,  # Use the subject from Excel or default from the email object
                    body=email_content,
                    to=[email_address],
                )

                # Add attachments to the email
                for attachment in attachments:
                    attachment_file_path = attachment.file.path
                    email_msg.attach_file(attachment_file_path)

                # Send the email
                try:
                    email_msg.send(fail_silently=False)
                    print(f"Email sent to {email_address}")
                except Exception as e:
                    print(f"Failed to send email to {email_address}: {e}")

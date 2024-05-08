# cargo/tasks.py

from celery import shared_task
from django.utils import timezone
from cargo.models import Enquiry

@shared_task
def send_pending_enquiry_notifications():
    pending_enquiries = Enquiry.objects.filter(status='pending')
    for enquiry in pending_enquiries:
        created_time = enquiry.created_at
        if (timezone.now() - created_time).total_seconds() >= 24 * 60 * 60:
            # Send notification (you can implement this part based on your notification mechanism)
            print(f"Sending notification to {enquiry.salesman} for pending enquiry #{enquiry.id}")

@shared_task
def delete_old_pending_enquiries():
    pending_enquiries = Enquiry.objects.filter(status='pending')
    for enquiry in pending_enquiries:
        created_time = enquiry.created_at
        if (timezone.now() - created_time).total_seconds() >= 48 * 60 * 60:
            # Delete the enquiry
            enquiry.delete()
            print(f"Deleted old pending enquiry #{enquiry.id}")




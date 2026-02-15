from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from .models import Event, Enrollment
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_followup_email():
    """
    Send follow-up email to seekers 1 day after event ends.
    """
    # Find events that ended exactly 1 day ago?
    # Or ended between 24h and 25h ago?
    # Better: ended within last 24h and email not sent?
    # Requirement: "1 day post-event".
    
    # Let's find events ended between 24h and 25h ago to avoid duplicate sending if run hourly.
    now = timezone.now()
    start_window = now - timedelta(days=1, hours=1)
    end_window = now - timedelta(days=1)
    
    events = Event.objects.filter(ends_at__gte=start_window, ends_at__lt=end_window)
    
    for event in events:
        enrollments = event.enrollments.filter(status='CONFIRMED')
        for enrollment in enrollments:
            logger.info(f"Sending followup to {enrollment.seeker.email} for event {event.title}")
            # Mock sending email
            print(f"=======================================")
            print(f"EMAIL TO: {enrollment.seeker.email}")
            print(f"SUBJECT: Followup on {event.title}")
            print(f"BODY: Hope you enjoyed the event!")
            print(f"=======================================")

@shared_task
def send_reminder_email():
    """
    Send reminder email to seekers 6 hours before event starts.
    """
    now = timezone.now()
    start_window = now + timedelta(hours=6)
    end_window = now + timedelta(hours=7)
    
    events = Event.objects.filter(starts_at__gte=start_window, starts_at__lt=end_window)
    
    for event in events:
        enrollments = event.enrollments.filter(status='CONFIRMED')
        for enrollment in enrollments:
            logger.info(f"Sending reminder to {enrollment.seeker.email} for event {event.title}")
            # Mock sending email
            print(f"=======================================")
            print(f"EMAIL TO: {enrollment.seeker.email}")
            print(f"SUBJECT: Reminder for {event.title}")
            print(f"BODY: Event starts in 6 hours!")
            print(f"=======================================")

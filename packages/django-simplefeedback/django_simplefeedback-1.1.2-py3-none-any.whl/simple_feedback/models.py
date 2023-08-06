from django.db import models
from django.db.models.signals import post_save
from django.core import mail
from django.contrib.auth.models import User
from django.template import loader
from django.dispatch import receiver
from django.conf import settings

# This has to stay here to use the proper celery instance with the djcelery_email package
try:
    import scheduler.celery  # noqa
except ImportError:
    pass


class Ticket(models.Model):
    STATUS_CHOICES = (
        ('New', 'New'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    )

    status = models.CharField(
        max_length=255,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES[0][0],
        blank=True,
        null=True
    )
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)  # anonym if empty
    assignee = models.ForeignKey(User, blank=True, null=True, related_name='tickets', on_delete=models.SET_NULL)
    email = models.EmailField(blank=True, null=True)
    subject = models.TextField()
    text = models.TextField()
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    modified = models.DateTimeField(auto_now=True, auto_now_add=False)
    meta = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.subject


@receiver(post_save, sender=Ticket)
def new_ticket_notification(sender, instance, created, **kwargs):
    if created:
        emails_to_notify = []
        if getattr(settings, 'SIMPLE_FEEDBACK_SEND_TO', False):
            if isinstance(settings.SIMPLE_FEEDBACK_SEND_TO, str):
                emails_to_notify = [settings.SIMPLE_FEEDBACK_SEND_TO]
            elif isinstance(settings.SIMPLE_FEEDBACK_SEND_TO, list):
                for email in settings.SIMPLE_FEEDBACK_SEND_TO:
                    if isinstance(email, str):
                        emails_to_notify.append(email)

        if not emails_to_notify:
            emails_to_notify = list(User.objects.filter(is_superuser=True).values_list('email', flat=True))
        html_template = loader.get_template("email/notify_template.html")
        html_message = html_template.render({'ticket': instance})

        if getattr(settings, 'SIMPLE_FEEDBACK_SEND_MAIL_FUNC_OVERRIDE', False):
            getattr(settings, 'SIMPLE_FEEDBACK_SEND_MAIL_FUNC_OVERRIDE')(message=html_message,
                                                                         recipients=emails_to_notify)
        else:
            mail.send_mail(
                subject='New ticket has been submitted',
                message='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=emails_to_notify,
                html_message=html_message,
                fail_silently=True)

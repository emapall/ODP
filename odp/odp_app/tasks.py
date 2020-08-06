from django.core.mail import send_mail

from django.conf import settings

from background_task import background


DEFAULT_MAIL_SENDER = settings.EMAIL_HOST_USER

@background(schedule=10)
def send_simple_email(sub,msg,to,sender=None):
    if not sender:
        sender = DEFAULT_MAIL_SENDER
    send_mail(sub,msg,sender,to,fail_silently = False)
    
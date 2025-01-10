from django.db.models.signals import post_save
from django.conf import settings
from django.dispatch import receiver
from .models import otpToken
from django.core.mail import send_mail
from django.utils import timezone


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_token(sender, instance, created, **kwargs):
    if created:
        if instance.is_superuser:
            pass
        else:
            otp = otpToken.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            instance.is_active = False
            instance.save()

            if otp:
                subject = "Email Verification"
                message = f"""
                    Hi {instance.username}, here is your OTP {otp.otp_code}
                    it expires in 5 minutes, use the URL below to redirect back to the website:
                    http://127.0.0.1:8000/user/verify-email/{instance.username}
                """
                
                sender = "taskmanagerprojectmail@gmail.com"
                receiver = [instance.email]

                send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False
                )


# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_token(sender, instance, created, **kwargs):

#     if created:
        
#         if instance.is_superuser:
#             pass

#         else:
#             otpToken.objects.create(user=instance, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
#             instance.is_active = False
#             instance.save()

#         otp = otpToken.objects.filter(user=instance).last()

#         subject = "Email Verification"
#         message = f"""

#                                 Hi {instance.username}, here is your OTP {otp.otp_code}
#                                 it Exprires in 5 minutes, use url below  redirect back to the website
#                                 http://127.0.0.1:8000/user/verify-email/{instance.username}
#                                 """
        
#         sender = "taskmanagerprojectmail@gmail.com"
#         receiver = [instance.email, ]


         
#         send_mail(
#             subject,
#             message,
#             sender,
#             receiver,
#             fail_silently=False
#         )

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import secrets

class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    username = models.CharField(max_length=100)
    team_lead = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
    
class otpToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="otps")
    otp_code = models.CharField(max_length=6, default=secrets.token_hex(3))
    otp_created_at = models.DateTimeField(auto_now_add=True)
    otp_expires_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.user.username
    


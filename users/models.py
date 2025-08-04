from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from .manager import UserManager

class User(AbstractUser, PermissionsMixin):
    username = None  
    email = models.EmailField(max_length=225, unique=True, verbose_name="Email Address")

    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"    
    REQUIRED_FIELDS = []          

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        from rest_framework_simplejwt.tokens import RefreshToken
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }


class OneTimePassword(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, unique=True)

    def __str__(self):
        return f"{self.user.email} - passcode"

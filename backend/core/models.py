from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

# User Manager


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, username=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")
        if not username:
            raise ValueError("Username is required")

        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', True)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, username, **extra_fields)

    def get_by_natural_key(self, email):
        return self.get(email=email)


# --------------------------------------------#

class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, null=False, unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

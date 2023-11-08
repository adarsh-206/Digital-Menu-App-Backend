# authentication/user.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from oauth2_provider.models import Application
from django.utils import timezone
from restaurants.models import Restaurant


class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, email=None, password=None):
        user = self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email) if email else None,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, email=None, password=None):
        return self.create_user(mobile_number, email, password)


class User(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(unique=True, max_length=10)
    email = models.EmailField(blank=True, null=True)
    last_login = models.DateTimeField(default=timezone.now)

    # A User can be associated with a Restaurant, and a Restaurant can be associated with multiple User objects
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, null=True, related_name='user_restaurant')

    objects = CustomUserManager()

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELD = []

    def __str__(self):
        return self.mobile_number

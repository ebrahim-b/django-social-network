from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **other_fields):
        if not phone:
            raise ValueError("Mobile is required")
        user = self.model(phone=phone, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone, password=None, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('is_staff in admin must True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser in admin must True')
        return self.create_user(phone, password, **other_fields)

class User(AbstractUser):
    # r'^[0][9]\d{9}$|^[1-9]\d{9}$'
    # r'^\+?1?\d{11}$'
    username = None
    phone_regex = RegexValidator(regex = r'^[0][9]\d{9}$|^[1-9]\d{9}$',
            message = 'Phone number up to 11 digits allowed start with 09')
    phone = models.CharField(validators = [phone_regex], max_length = 11,unique=True)
    token = models.CharField(max_length=64,blank=True, null=True)
    token_expiration_date = models.DateTimeField(null=True)
    salt = models.CharField(max_length=32, null=True)

    object = UserManager()

    USERNAME_FIELD = 'phone'

    REQUIRED_FIELDS = []

    backend = 'accounts.custombackend.PhoneBackend'

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.core.validators import RegexValidator



phone_regex = RegexValidator(regex = r'^\+?1?\d{9-14}$',
            message = 'Phone number up to 14 digits allowed')


class UserManager(BaseUserManager):
    def create_user(self, phone, password = None, is_active = False, is_admin = False):
        if not phone:
            raise ValueError('User must have a phone number')
        if not password:
            raise ValueError('User must have a password')

        user_obj = self.model(
            phone = phone
        )
        user_obj.set_password(password)
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)
        return user_obj

    def create_superuser(self,phone,password=None):
        user = self.create_user(
            phone,
            password=password,
            is_admin = True,
            is_active = True
        )

        return user

class User(AbstractBaseUser):
    phone = models.CharField(validators = [phone_regex], max_length = 15,)
    full_name = models.CharField(max_length = 60, blank =True, null = True)
    first_login = models.BooleanField(default=False)
    active   = models.BooleanField(default=False)
    admin    = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add = True)


    USERNAME_FIELD = 'phone'
    REQURED_FIELDS = []

    object = UserManager()


    def __str__(self):
        return self.phone

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        else:
            return self.phone

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

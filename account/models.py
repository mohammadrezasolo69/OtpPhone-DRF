from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message=_("Invalid phone number."))


class UserManager(BaseUserManager):
    def _create_user(self, phone, password, **extra_field):
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_field)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password, **extra_field):
        """ Create and save a user with the given phone. """
        extra_field.setdefault('is_staff', False)
        extra_field.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_field)

    def create_superuser(self, phone, password, **extra_fields):
        """ Create and save a super user with the given phone_number. """

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    phone = models.CharField(max_length=11, validators=[phone_regex], unique=True)
    is_phone_verified = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']


class OTP(models.Model):
    phone = models.CharField(max_length=11, validators=[phone_regex])
    otp = models.CharField(max_length=6, )
    created_at = models.DateTimeField(auto_now_add=True)

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, username, phone_number=None, password=None, role='staff',
                    **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have an username')
        if not first_name:
            raise ValueError('Users must have a first name')
        if not last_name:
            raise ValueError('Users must have a last name')

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, username=username,
                          phone_number=phone_number, role=role, **extra_fields)
        user.set_password(password)  # for hash pw
        user.save(using=self._db)  # save user to database
        return user

    def create_superuser(self, email, first_name='', last_name='', username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email=email, first_name=first_name, last_name=last_name, username=username,
                                phone_number=None, password=password, role='admin',
                                **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=255, unique=True)
    phone_number = PhoneNumberField(region='KH', unique=True)
    role = models.CharField(max_length=255, choices=ROLE_CHOICES, default='staff')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} ({self.role})"

# test endpoint, create git repo

import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


# Custom User, because we need email to authentication not username
class User(AbstractUser):
    password = models.CharField(max_length=100)
    is_verified = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=36, blank=True)
    objects = UserManager()

    username = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def activate_with_code(self, code):
        if str(self.activation_code) != str(code):
            raise Exception(_('code does not match'))
        self.is_active = True
        self.activation_code = ''
        self.save(update_fields=['is_active', 'activation_code'])

    def create_activation_code(self):
        code = str(uuid.uuid4())
        self.activation_code = code

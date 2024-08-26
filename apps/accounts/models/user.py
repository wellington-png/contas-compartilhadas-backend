from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from apps.core.models import BaseModel


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email address must be provided")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModel):
    username = None
    email = models.EmailField("Email", unique=True)
    name = models.CharField("Name", max_length=255)
    fixed_income = models.DecimalField(
        "Fixed Income",
        max_digits=10,
        decimal_places=2,
        default=0.00,
    )
    ACCOUNT_TYPE_CHOICES = (
        ("Simple", "Simple"),
        ("Prime", "Prime"),
    )
    account_type = models.CharField(
        "Account Type", max_length=10, choices=ACCOUNT_TYPE_CHOICES, default="Simple"
    )
    
    avatar = models.CharField("Avatar", max_length=50, default="default")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

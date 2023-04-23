from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from helpers.files import ValidateFileSize


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, password, **kwargs):
        email = self.normalize_email(email=email)
        user = self.model(email=email, first_name=first_name, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)
        return self.create_user(email=email, first_name=first_name, **kwargs)


class User(AbstractUser):
    """
    This model is used to store user details.
    """

    username = None
    email = models.EmailField(max_length=256, unique=True)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, null=True, blank=True)
    is_seller = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name"]

    objects = UserManager()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return (self.first_name.strip() + " " + (self.last_name or "").strip()).rstrip()

    def validate_user_type(self):
        if not (self.is_seller or self.is_buyer):
            raise ValidationError("User must be seller or buyer.")

    def clean(self):
        self.validate_user_type()


class Profile(models.Model):
    MAX_FILE_SIZE_ALLOWED = 5  # MB
    EXTENSIONS_ALLOWED = ("jpeg", "png", "jpg")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(
        validators=[
            ValidateFileSize(max_file_size=MAX_FILE_SIZE_ALLOWED),
            FileExtensionValidator(allowed_extensions=EXTENSIONS_ALLOWED),
        ],
        null=True,
        blank=True,
    )
    pan_card = models.CharField(null=True, blank=True, max_length=10)
    aadhar_card = models.CharField(null=True, blank=True, max_length=12)
    address = models.TextField()

    def __str__(self):
        return f"{self.user.email}'s Profile"

    def clean(self) -> None:
        return super().clean()

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now

from helpers.files import RenameFile, ValidateFileSize, file_storage
from properties.tasks import send_emails_task
from users.models import User


class Property(models.Model):
    """
    Model to store properties information to be auctioned.
    """

    name = models.CharField(max_length=256)
    seller = models.ForeignKey(User, on_delete=models.PROTECT)
    location = models.TextField()
    base_price = models.PositiveBigIntegerField(
        validators=[MinValueValidator(10000)]
    )  # in INR
    start_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Property"
        verbose_name_plural = "Properties"

    def __str__(self) -> str:
        return self.name

    def validate_dates(self):
        if self.start_date < now():
            raise ValidationError("Start date must be greater than present.")

        if self.start_date > self.closing_date:
            raise ValidationError("Closing date must be greater than start date.")

    def clean(self):
        self.validate_dates()

    def full_clean(self, exclude=None, validate_unique=True) -> None:
        breakpoint()
        if self.pk and self.is_active:
            initial_instance = Property.objects.get(id=self.pk)
            if not initial_instance.is_active:
                send_emails_task.delay(property_id=self.pk)

        return super().full_clean(exclude, validate_unique)

    def save(self, *args, **kwargs):
        skip_clean = kwargs.pop("skip_clean", False)
        if not skip_clean:
            self.full_clean(exclude=kwargs.pop("exclude_clean", None))
        return super().save(*args, **kwargs)


class PropertyGallery(models.Model):
    """
    Model to store property images or videos to be auctioned.
    """

    MAX_FILE_ALLOWED = 5
    MAX_FILE_SIZE_ALLOWED = 5  # MB
    EXTENSIONS_ALLOWED = ("jpeg", "png", "jpg")

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    file = models.FileField(
        validators=[
            ValidateFileSize(max_file_size=MAX_FILE_SIZE_ALLOWED),
            FileExtensionValidator(allowed_extensions=EXTENSIONS_ALLOWED),
        ],
    )

    class Meta:
        verbose_name = "Property Gallery"
        verbose_name_plural = "Property Gallery"

    def __str__(self) -> str:
        return f"{self.pk} {self.property.name}"

    def validate_file_count(self):
        if (
            PropertyGallery.objects.filter(property_id=self.property_id).count()
            > self.MAX_FILE_ALLOWED
        ):
            raise ValidationError("Max file limit reached.")

    def full_clean(self, exclude, validate_unique):
        super().full_clean(exclude, validate_unique)
        self.validate_file_count()

    def save(self, *args, **kwargs):
        skip_clean = kwargs.pop("skip_clean", False)
        if not skip_clean:
            self.full_clean(exclude=kwargs.pop("exclude_clean", None))
        return super().save(*args, **kwargs)


class PropertyDocument(models.Model):
    """
    Model to store property documents to be auctioned.
    """

    MAX_DOCUMENT_ALLOWED = 5
    MAX_FILE_SIZE_ALLOWED = 5  # MB
    EXTENSIONS_ALLOWED = ("pdf", "jpeg", "png", "jpg")

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    document = models.FileField(
        validators=[
            ValidateFileSize(max_file_size=MAX_FILE_SIZE_ALLOWED),
            FileExtensionValidator(allowed_extensions=EXTENSIONS_ALLOWED),
        ],
    )
    description = models.TextField()

    class Meta:
        verbose_name = "Property Document"
        verbose_name_plural = "Property Documents"

    def __str__(self) -> str:
        return f"{self.pk} {self.property.name}"

    def validate_file_count(self):
        if (
            PropertyDocument.objects.filter(property_id=self.property_id).count()
            > self.MAX_DOCUMENT_ALLOWED
        ):
            raise ValidationError("Max document limit reached.")

    def full_clean(self, exclude, validate_unique):
        super().full_clean(exclude, validate_unique)
        self.validate_file_count()

    def save(self, *args, **kwargs):
        skip_clean = kwargs.pop("skip_clean", False)
        if not skip_clean:
            self.full_clean(exclude=kwargs.pop("exclude_clean", None))
        return super().save(*args, **kwargs)

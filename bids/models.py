from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from properties.models import Property
from users.models import User


class Auction(models.Model):
    property = models.ForeignKey(Property, on_delete=models.PROTECT)
    buyer = models.ForeignKey(User, on_delete=models.PROTECT)
    amount = models.PositiveBigIntegerField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=now)

    class Meta:
        verbose_name = "Auction"
        verbose_name_plural = "Auctions"

    def __str__(self) -> str:
        return f"{self.property.name} - {self.amount}"

    def validate_auction(self):
        if not self.property.start_date < now() < self.property.closing_date:
            raise ValidationError(
                "Bidding date and time must be in between auction start date and closing date."
            )

    def validate_amount(self):
        if self.amount <= (
            Auction.objects.filter(property=self.property, is_active=True)
            .order_by("-amount")
            .first()
            or 0
        ):
            raise ValidationError("Bidding amount must be greater than highest amount.")

    def full_clean(self, exclude, validate_unique):
        super().full_clean(exclude, validate_unique)
        self.validate_auction()
        self.validate_amount()

    def save(self, *args, **kwargs):
        skip_clean = kwargs.pop("skip_clean", False)
        if not skip_clean:
            self.full_clean(exclude=kwargs.pop("exclude_clean", None))
        return super().save(*args, **kwargs)

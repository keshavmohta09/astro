from os import environ

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils.timezone import now

from users.models import User


@shared_task()
def send_emails_task(property_id: int):
    from properties.models import Property

    try:
        property = Property.objects.get(id=property_id)
    except Property.DoesNotExist:
        raise Exception(f"<Property: {property_id}> not found")

    email_subject = f"Bidder | New Property - {property.name}"
    email_message = f"""Hey,
New property is ready for auction.
Property Details: 
    Name: {property.name}
    Seller: {property.seller.full_name}
    Ask Price: {property.base_price}
    Auction Start Date: {property.start_date}
    Auction Closing Date: {property.closing_date}
    Location: {property.location}

Best regards,
Team Bidder
"""
    users = list(User.objects.filter(is_buyer=True).values_list("email", flat=True))
    send_mail(
        subject=email_subject,
        message=email_message,
        recipient_list=users,
        from_email="noreply@bidder.com",
        auth_user=settings.EMAIL_HOST_USER,
        auth_password=settings.EMAIL_HOST_PASSWORD,
    )


@shared_task()
def mark_inactive_property():
    from bids.models import Auction
    from properties.models import Property

    properties = Property.objects.filter(is_active=True, closing_date__lte=now())
    email_subject = f"Bidder | Congratulations"
    buyer_message = """Hey,
Congratulations, you win the auction
Property Details: 
    Name: {property.name}
    Seller: {property.seller.full_name}
    Ask Price: {property.base_price}
    Auction Start Date: {property.start_date}
    Auction Closing Date: {property.closing_date}
    Location: {property.location}

Contact the seller for more information:
    Seller email: {property.seller.email}


Best regards,
Team Bidder
"""
    seller_message = """Hey,
Congratulations, you auction is closed.

Contact the buyer for more information:
    Buyer email: {bid.buyer.email}
    Amount: {bid.amount}


Best regards,
Team Bidder
"""

    properties.update(is_active=False)
    for property in properties:
        bid = Auction.objects.filter(is_active=True).order_by("-amount").first()
        if bid:
            send_mail(
                subject=email_subject,
                message=seller_message.format(bid=bid),
                from_email="noreply@bidder.com",
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
            )
            send_mail(
                subject=email_subject,
                message=buyer_message.format(property=property),
                from_email="noreply@bidder.com",
                auth_user=settings.EMAIL_HOST_USER,
                auth_password=settings.EMAIL_HOST_PASSWORD,
            )

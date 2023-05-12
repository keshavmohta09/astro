from django.urls import path

from properties.views import ListRunningAuctionsAPI

urlpatterns = [
    path(
        "running-auctions/",
        ListRunningAuctionsAPI().get,
        name="list-running-auctions",
    ),
]

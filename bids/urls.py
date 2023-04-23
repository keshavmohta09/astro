from django.urls import path

from bids.views import CreateBidAPI

urlpatterns = [
    path("create/", CreateBidAPI.as_view(), name="create-bid"),
]

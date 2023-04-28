from django.urls import path

from bids.views import CreateBidAPI

urlpatterns = [
    path("create/", CreateBidAPI().create, name="create-bid"),
]

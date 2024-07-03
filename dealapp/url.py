from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("create_deal", views.create_deal),
    path("update_deal", views.update_deal),
    path("end_deal", views.end_deal),
    path("claim_deal", views.claim_deal),
    path("show_deals", views.show_deals),
    path("show_users", views.show_users),
]

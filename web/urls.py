from django.urls import path

from . import views

app_name = "web"
urlpatterns = [
    path("", views.index, name="index"),
    path("membership", views.membership, name="membership"),
    path("events-meetings", views.events_meetings, name="events_meetings"),
    path("resources", views.resources, name="resources"),
    path("resources/technical", views.technical_resources, name="technical_resources"),
    path("resources/funding", views.funding_resources, name="funding_resources"),
    path("resources/partner-orgs", views.partner_orgs, name="partner_orgs"),
    path("search", views.search, name="search"),
]

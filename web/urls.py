from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "web"
urlpatterns = [
    path("", views.index, name="index"),
    path("membership", views.membership, name="membership"),
    path("strategic-plan", views.strategic_plan, name="strategic_plan"),
    path("events-meetings", views.events_meetings, name="events_meetings"),
    path("resources", views.resources, name="resources"),
    path("resources/technical", views.technical_resources, name="technical_resources"),
    path("resources/funding", views.funding_resources, name="funding_resources"),
    path("resources/partner-orgs", views.partner_orgs, name="partner_orgs"),
    path("search", views.search, name="search"),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name="about"),
    path('membership', views.membership, name="membership"),
    path('events-meetings', views.events_meetings, name="events_meetings"),
    path('events-meetings/<int:meeting_id>', views.meeting_detail, name="meeting_detail"),
    path('resources', views.resources, name="resources"),
    path('resources/technical', views.technical_resources, name="technical_resources"),
    path('resources/funding', views.funding_resources, name="funding_resources"),
    path('contact', views.contact, name="contact"),
    path('search', views.search, name="search"),
]

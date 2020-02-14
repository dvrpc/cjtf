from django.urls import path

from . import views

app_name = 'web'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name="about"),
    path('membership/', views.membership, name="membership"),
    path('events-meetings/', views.EventsIndexView.as_view(), name="events"),
    path('events-meetings/<int:event_id>/', views.event_details, name="event_detail"),
    path('resources/', views.resources, name="resources"),
    path('contact/', views.contact, name="contact"),
]

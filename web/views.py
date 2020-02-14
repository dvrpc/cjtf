from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Event, Page


def index(request):
    context = {
        'title': 'Central Jersey Transportation Forum'
    }
    return render(request, 'web/home.html', context)


def about(request):
    page = get_object_or_404(Page, internal_name="about")

    context = {
        'title': page.title,
        'page': page,
    }
    return render(request, 'web/default.html', context)


def membership(request):
    context = {
        'title': 'Membership'
    }
    return render(request, 'web/default.html', context)


class EventsIndexView(generic.ListView):
    """List of all events, using Django's generic index view"""

    template_name = 'web/events.html'
    context_object_name = 'events'
    queryset = Event.objects.order_by('-date')

    def get_context_data(self, **kwargs):
        """Overwrite in order to add additional variable (title) in context"""
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['title'] = "Meetings and Events"
        return context


def event_details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    context = {
        'event': event,
        'title': event.title,
    }
    return render(request, 'web/event_detail.html', context)


def resources(request):
    context = {
        'title': 'Resources'
    }
    return render(request, 'web/resources.html', context)


def contact(request):
    page = get_object_or_404(Page, internal_name="contact")
    context = {
        'title': page.title,
        'page': page,
    }
    return render(request, 'web/default.html', context)

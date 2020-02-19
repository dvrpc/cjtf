import datetime

from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views import generic

from .models import Event, Page, TechnicalResource, FundingResource


def index(request):
    """
    Home Page. Get recently updated internal pages (events/meetings and resources) and also
    set up the Twitter list feed.
    """
    
    
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
    page = get_object_or_404(Page, internal_name="membership")
    context = {
        'title': 'Membership'
    }
    return render(request, 'web/default.html', context)


def events(request):
    page = get_object_or_404(Page, internal_name="events_meetings")
    upcoming_events = Event.objects.filter(date__gte=datetime.date.today())
    past_events = Event.objects.filter(date__lt=datetime.date.today())

    context = {
        'title': page.title,
        'page': page,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
    }
    return render(request, 'web/default.html', context)


def event_details(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    context = {
        'event': event,
        'title': event.title,
    }
    return render(request, 'web/event_detail.html', context)


def resources(request):

    page = get_object_or_404(Page, internal_name="resources")
    context = {
        'title': page.title,
        'page': page,
    }
    return render(request, 'web/default.html', context)


def technical_resources(request):

    categories = TechnicalResource._meta.get_field('category').choices
    technical_resources = TechnicalResource.objects.all()
    context = {
        'title': 'Technical Resources',
        'resources': technical_resources,
        'categories': categories,
    }
    return render(request, 'web/resources_technical.html', context)


def funding_resources(request):
    resources = FundingResource.objects.filter(due_date__gte=datetime.datetime.today()).order_by('due_date')
    context = {
        'title': 'Funding Resources',
        'resources': resources,
    }
    return render(request, 'web/resources_funding.html', context)



def contact(request):
    page = get_object_or_404(Page, internal_name="contact")
    context = {
        'title': page.title,
        'page': page,
    }
    return render(request, 'web/default.html', context)

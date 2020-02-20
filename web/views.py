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
    
    category = request.GET.get('category', '')

    if category in ['regional_plans', 'municipal_tools', 'research_and_reports']:
        technical_resources = TechnicalResource.objects.filter(category=category)
    else:
        technical_resources = TechnicalResource.objects.all()

    # get and send the page so we can include the same sidebar across all resources pages
    page = get_object_or_404(Page, internal_name="resources")
    
    context = {
        'title': 'Technical Resources',
        'page': page,
        'resources': technical_resources,
        'category': category,
    }
    return render(request, 'web/resources.html', context)


def funding_resources(request):
    
    funding_resources = FundingResource.objects.filter(
        due_date__gte=datetime.datetime.today()
    ).order_by('due_date')
    
    # get and send the page so we can include the same sidebar across all resources pages
    page = get_object_or_404(Page, internal_name="resources")
    
    context = {
        'title': 'Funding Resources',
        'resources': funding_resources,
        'page': page,
    }
    return render(request, 'web/resources.html', context)



def contact(request):
    page = get_object_or_404(Page, internal_name="contact")
    context = {
        'title': page.title,
        'page': page,
    }
    return render(request, 'web/default.html', context)

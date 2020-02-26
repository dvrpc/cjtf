import datetime

from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views import generic

from .models import Event, Page, TechnicalResource, FundingResource


def index(request):
    '''
    Home Page. Get recently updated internal pages (events/meetings and resources) and also
    set up the Twitter list feed.
    '''

    # Get various new/updated resources to display.
    
    six_weeks_ago = datetime.date.today() - datetime.timedelta(days=14)

    # get the event/meeting coming up next, if any
    try:
        next_event = Event.objects.filter(date__gte=datetime.date.today()).order_by('date').first()
    except Event.DoesNotExist:
        next_event = None

    # get 3 newest technical resources (3 at most)
    tech_resources = (TechnicalResource
        .objects.filter(publication_date__gte=six_weeks_ago)
        .order_by('publication_date')[0:3])   

    # get at most 3 funding resources that are coming up
    funding_resources = (FundingResource
        .objects.filter(due_date__gte=datetime.date.today())
        .order_by('due_date')[0:3])

    # get any newly added meeting minutes/highlights
    updated_meetings = (Event
        .objects
        .filter(minutes_added__gte=six_weeks_ago)
        .exclude(minutes='')
        .order_by('minutes_added')[0:3])
    
    context = {
        'title': 'Central Jersey Transportation Forum',
        'next_event': next_event,
        'tech_resources': tech_resources,
        'funding_resources': funding_resources,
        'updated_meetings': updated_meetings,
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
    return render(request, 'web/resources.html', context)


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

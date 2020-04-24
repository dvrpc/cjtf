import datetime
from itertools import chain

from django.db.models import Q
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.views import generic

from .models import Meeting, Event, Page, TechnicalResource, FundingResource


def index(request):
    '''
    Home Page. Get recently updated internal pages (events/meetings and resources) and also
    set up the Twitter list feed.
    '''

    # how far back to check for added tech resources or added meeting minutes/presentations
    six_weeks_ago = datetime.date.today() - datetime.timedelta(days=14)

    try:
        next_meeting = Meeting.objects.filter(date__gte=datetime.datetime.now()).order_by('date').first()
    except Meeting.DoesNotExist:
        next_meeting = None

    upcoming_events = Event.objects.filter(date__gte=datetime.datetime.now()).order_by('date')[0:3]

    tech_resources = (TechnicalResource
        .objects.filter(publication_date__gte=six_weeks_ago)
        .order_by('publication_date')[0:3])   

    funding_resources = (FundingResource
        .objects.filter(due_date__gte=datetime.date.today())
        .order_by('due_date')[0:3])
    
    # get meetings with newly added minutes or presentation materials; exclude those that have
    # no values for the file field (because the "added" fields will be updated whether files are
    # added or deleted)
    # Note that this orders by most recent date of meeting - not date of when these were added,
    # but that's ok because we don't really need to highlight updated materials from very old 
    # meetings, if that should every happen
    meetings_updated = (Meeting
        .objects
        .filter(
            (Q(minutes_added__gte=six_weeks_ago) & ~Q(minutes='')) |
            (Q(pre_mat_added__gte=six_weeks_ago) & ~Q(presentation_materials=''))
        ) 
        .order_by('-date')[0:3])

    context = {
        'title': 'Central Jersey Transportation Forum',
        'next_meeting': next_meeting,
        'tech_resources': tech_resources,
        'funding_resources': funding_resources,
        'meetings_updated': meetings_updated,
        'upcoming_events': upcoming_events,
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
        'title': page.title,
        'page': page,
    }
    return render(request, 'web/default.html', context)


def events_meetings(request):
    page = get_object_or_404(Page, internal_name="events_meetings")
    upcoming_events = Event.objects.filter(date__gte=datetime.datetime.now()).order_by('date')
    upcoming_meetings = Meeting.objects.filter(date__gte=datetime.datetime.now()).order_by('date')
    past_meetings = Meeting.objects.filter(date__lt=datetime.date.today()).order_by('-date')

    # so we can order by date regardless if thing is an event or meeting, combine upcoming
    # meetings and upcoming events into one list and sort

    # first, since meetings don't have titles, add one
    # for meeting in upcoming_meetings:
    #     meeting.title = "Forum Regular Meeting"  
    #     
    # upcoming_events_meetings = sorted(chain(upcoming_events, upcoming_meetings), 
    #     key=lambda x: x.date)

    # so it's easy to display in template, give the latest past meeting for each year a 'year' attribute
    current_year = ''
    for past_meeting in past_meetings:
        if not current_year or current_year != past_meeting.date.year: 
            past_meeting.year = past_meeting.date.year
            current_year = past_meeting.date.year
        else:
            past_meeting.year = ''

    context = {
        'title': page.title,
        'page': page,
        'upcoming_events': upcoming_events,
        'upcoming_meetings': upcoming_meetings, 
        'past_meetings': past_meetings,
    }
    return render(request, 'web/default.html', context)


def meeting_detail(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    context = {
        'meeting': meeting,
        'title': "Regular Meeting",
    }
    return render(request, 'web/meeting_detail.html', context)


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

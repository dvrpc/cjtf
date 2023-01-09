import datetime

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from django.shortcuts import get_object_or_404, render

import django_tables2 as tables

from .models import Meeting, Event, Page, TechnicalResource, FundingResource
from .tables import TechnicalResourceTable, FundingResourceTable


def index(request):
    """
    Home Page. Get recently updated internal pages (events/meetings and resources).
    """

    # get next and most recent meeting
    try:
        next_meeting = (
            Meeting.objects.filter(date__gte=datetime.datetime.now()).order_by("date").first()
        )
    except Meeting.DoesNotExist:
        next_meeting = None

    try:
        last_meeting = (
            Meeting.objects.filter(date__lt=datetime.datetime.now()).order_by("-date").first()
        )
    except Meeting.DoesNotExist:
        last_meeting = None

    upcoming_events = Event.objects.filter(
        Q(start_date__gte=datetime.date.today()) | Q(end_date__gte=datetime.date.today())
    ).order_by("start_date")[0:3]

    # exclude tech resources without pdf and without url, because what's the use of including it?
    tech_resources = TechnicalResource.objects.exclude(
        Q(url__isnull=True) & Q(pdf__isnull=True)
    ).order_by("-publication_date")[0:3]

    funding_resources = FundingResource.objects.filter(
        due_date__gte=datetime.date.today()
    ).order_by("due_date")[0:3]

    context = {
        "title": "Central Jersey Transportation Forum",
        "next_meeting": next_meeting,
        "tech_resources": tech_resources,
        "funding_resources": funding_resources,
        "last_meeting": last_meeting,
        "upcoming_events": upcoming_events,
    }
    return render(request, "web/home.html", context)


def membership(request):
    page = get_object_or_404(Page, internal_name="membership")
    context = {
        "title": page.title,
        "page": page,
    }
    return render(request, "web/default.html", context)


def events_meetings(request):
    page = get_object_or_404(Page, internal_name="events_meetings")
    upcoming_events = Event.objects.filter(
        Q(start_date__gte=datetime.date.today()) | Q(end_date__gte=datetime.date.today())
    ).order_by("start_date")
    upcoming_meetings = Meeting.objects.filter(date__gte=datetime.datetime.now()).order_by("date")
    past_meetings = Meeting.objects.filter(date__lt=datetime.date.today()).order_by("-date")

    context = {
        "title": page.title,
        "page": page,
        "upcoming_events": upcoming_events,
        "upcoming_meetings": upcoming_meetings,
        "past_meetings": past_meetings,
    }
    return render(request, "web/default.html", context)


def resources(request):

    page = get_object_or_404(Page, internal_name="resources")
    context = {
        "title": page.title,
        "page": page,
    }
    return render(request, "web/resources.html", context)


def technical_resources(request):

    category = request.GET.get("category", "")

    if category in ["regional_plans", "municipal_tools", "research_and_reports"]:
        technical_resources = TechnicalResource.objects.filter(category=category)
    else:
        technical_resources = TechnicalResource.objects.all()

    if technical_resources:
        technical_resources = TechnicalResourceTable(technical_resources)
        # set default sort for the table and configure it so sorting is enabled
        technical_resources.order_by = "-publication_date"
        tables.RequestConfig(request, paginate=False).configure(technical_resources)

    context = {
        "title": "Technical Resources",
        "resources": technical_resources,
        "category": category,
    }
    return render(request, "web/resources.html", context)


def funding_resources(request):

    # get all funding resources, excluding those in the past (using .exclude rather than .filter
    # (gte rather than lte) ensures that those without a due date are included)
    funding_resources = FundingResource.objects.exclude(due_date__lte=datetime.datetime.today())

    if funding_resources:
        funding_resources = FundingResourceTable(funding_resources)

        # set default sort for the table and configure it so sorting is enabled
        funding_resources.order_by = "due_date"
        tables.RequestConfig(request, paginate=False).configure(funding_resources)

    context = {
        "title": "Funding Resources",
        "resources": funding_resources,
    }
    return render(request, "web/resources.html", context)


def partner_orgs(request):
    page = get_object_or_404(Page, internal_name="partner_orgs")

    context = {
        "title": page.title,
        "page": page,
    }
    return render(request, "web/default.html", context)


def search(request):
    context = {
        "title": "Search",
    }

    if request.method == "GET":
        return render(request, "web/search.html", context)
    if request.method == "POST":
        search_term = request.POST.get("search_term", None)

        if not search_term:
            return render(request, "web/search.html", context)

        results = {}

        query = SearchQuery(search_term)

        # Pages
        vector = SearchVector("title", weight="A") + SearchVector(
            "main_content", "sidebar", weight="B"
        )
        pages = (
            Page.objects.annotate(search=vector, rank=SearchRank(vector, query))
            .filter(search=query)
            .order_by("-rank")
        )
        if pages.exists():
            results["pages"] = pages

        # Events
        vector = (
            SearchVector("title", weight="A")
            + SearchVector("description", weight="B")
            + SearchVector("location", weight="C")
        )
        events = (
            Event.objects.annotate(search=vector, rank=SearchRank(vector, query))
            .filter(search=query)
            .order_by("rank")
        )
        if events.exists():
            results["events"] = events

        # Technical Resources
        vector = (
            SearchVector("name", weight="A")
            + SearchVector("summary", weight="B")
            + SearchVector("source", weight="C")
        )
        tech_resources = (
            TechnicalResource.objects.annotate(search=vector, rank=SearchRank(vector, query))
            .filter(search=query)
            .order_by("rank")
        )

        if tech_resources.exists():
            results["tech_resources"] = tech_resources

        # Funding Resources
        vector = (
            SearchVector("name", weight="A")
            + SearchVector("description", weight="B")
            + SearchVector("source_name", weight="C")
        )
        funding_resources = (
            FundingResource.objects.annotate(search=vector, rank=SearchRank(vector, query))
            .filter(search=query)
            .exclude(due_date__lte=datetime.datetime.today())
            .order_by("rank")
        )
        if funding_resources.exists():
            results["funding_resources"] = funding_resources

        context.update(
            [("search_attempt", True), ("search_term", search_term), ("results", results)]
        )
        return render(request, "web/search.html", context)

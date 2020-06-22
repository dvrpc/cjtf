import datetime
import textwrap

from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.core.mail import send_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

import django_tables2 as tables

from .models import Meeting, Event, Page, TechnicalResource, FundingResource
from .forms import (
    TypeContactForm,
    CommentForm,
    EventForm,
    FundingResourceForm,
    TechnicalResourceForm,
)
from .tables import TechnicalResourceTable, FundingResourceTable


def index(request):
    """
    Home Page. Get recently updated internal pages (events/meetings and resources) and also
    set up the Twitter list feed.
    """

    # how far back to check for added tech resources or added meeting minutes/presentations
    six_weeks_ago = datetime.date.today() - datetime.timedelta(days=14)

    try:
        next_meeting = (
            Meeting.objects.filter(date__gte=datetime.datetime.now()).order_by("date").first()
        )
    except Meeting.DoesNotExist:
        next_meeting = None

    upcoming_events = Event.objects.filter(
        Q(start_date__gte=datetime.datetime.now()) | Q(end_date__gte=datetime.datetime.now())
    ).order_by("start_date")[0:3]

    # exclude tech resources without pdf and without url, because what's the use of including it?
    tech_resources = (
        TechnicalResource.objects.exclude(url__isnull=True)
        .exclude(pdf__isnull=True)
        .order_by("-publication_date")[0:3]
    )

    funding_resources = FundingResource.objects.filter(
        due_date__gte=datetime.date.today()
    ).order_by("due_date")[0:3]

    # get meetings with newly added minutes or presentation materials; exclude those that have
    # no values for the file field (because the "added" fields will be updated whether files are
    # added or deleted)
    # Note that this orders by most recent date of meeting - not date of when these were added,
    # but that's ok because we don't really need to highlight updated materials from very old
    # meetings, if that should every happen
    meetings_updated = Meeting.objects.filter(
        (Q(minutes_added__gte=six_weeks_ago) & ~Q(minutes=""))
        | (Q(pre_mat_added__gte=six_weeks_ago) & ~Q(presentation_materials=""))
    ).order_by("-date")[0:3]

    context = {
        "title": "Central Jersey Transportation Forum",
        "next_meeting": next_meeting,
        "tech_resources": tech_resources,
        "funding_resources": funding_resources,
        "meetings_updated": meetings_updated,
        "upcoming_events": upcoming_events,
    }
    return render(request, "web/home.html", context)


def about(request):
    page = get_object_or_404(Page, internal_name="about")

    context = {
        "title": page.title,
        "page": page,
    }
    return render(request, "web/default.html", context)


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
        Q(start_date__gte=datetime.datetime.now()) | Q(end_date__gte=datetime.datetime.now())
    ).order_by("start_date")
    upcoming_meetings = Meeting.objects.filter(date__gte=datetime.datetime.now()).order_by("date")
    past_meetings = Meeting.objects.filter(date__lt=datetime.date.today()).order_by("-date")

    # so it's easy to display in template, give the latest past meeting for each year a 'year' attribute
    current_year = ""
    for past_meeting in past_meetings:
        if not current_year or current_year != past_meeting.date.year:
            past_meeting.year = past_meeting.date.year
            current_year = past_meeting.date.year
        else:
            past_meeting.year = ""

    context = {
        "title": page.title,
        "page": page,
        "upcoming_events": upcoming_events,
        "upcoming_meetings": upcoming_meetings,
        "past_meetings": past_meetings,
    }
    return render(request, "web/default.html", context)


def meeting_detail(request, meeting_id):
    meeting = get_object_or_404(Meeting, pk=meeting_id)
    context = {
        "meeting": meeting,
        "title": "Regular Meeting",
    }
    return render(request, "web/meeting_detail.html", context)


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
        technical_resources = TechnicalResourceTable(
            TechnicalResource.objects.filter(category=category)
        )
    else:
        # technical_resources = TechnicalResource.objects.order_by("-publication_date").all()
        technical_resources = TechnicalResourceTable(TechnicalResource.objects.all())

    # set default sort for the table and configure it so sorting is enabled
    technical_resources.order_by = "-publication_date"
    tables.RequestConfig(request).configure(technical_resources)

    context = {
        "title": "Technical Resources",
        "resources": technical_resources,
        "category": category,
    }
    return render(request, "web/resources.html", context)


def funding_resources(request):

    # get all funding resources, excluding those in the past (using .exclude rather than .filter
    # (gte rather than lte) ensures that those without a due date are included)
    funding_resources = FundingResourceTable(
        FundingResource.objects.exclude(due_date__lte=datetime.datetime.today())
    )

    # set default sort for the table and configure it so sorting is enabled
    funding_resources.order_by = "due_date"
    tables.RequestConfig(request).configure(funding_resources)

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


def contact(request):
    if request.method == "POST":
        # determine which form was submitted - from name of submit button - and process
        if "submit_type" in request.POST:
            form = TypeContactForm(request.POST)
            if form.is_valid():

                f = form.cleaned_data
                if f["type_of_contact"] == "comment_or_question":
                    form = CommentForm()
                    submit_name = "submit_comment"
                    form_heading = "Submit a Comment or Question"
                elif f["type_of_contact"] == "event":
                    form = EventForm()
                    submit_name = "submit_event"
                    form_heading = "Submit an Event or Meeting"
                elif f["type_of_contact"] == "funding_resource":
                    form = FundingResourceForm()
                    submit_name = "submit_funding"
                    form_heading = "Submit a Funding Resource"
                elif f["type_of_contact"] == "technical_resource":
                    form = TechnicalResourceForm()
                    submit_name = "submit_technical"
                    form_heading = "Submit a Technical Resource"

                page = get_object_or_404(Page, internal_name="contact")
                context = {
                    "title": page.title,
                    "page": page,
                    "form": form,
                    "second_form": True,
                    "submit_name": submit_name,
                    "form_heading": form_heading,
                }
                return render(request, "web/contact.html", context)
        else:
            if "submit_comment" in request.POST:
                form = CommentForm(request.POST)
                if form.is_valid():
                    f = form.cleaned_data
                    submitted = "a comment or question"
                    body = f["comment"]
            if "submit_event" in request.POST:
                form = EventForm(request.POST)
                if form.is_valid():
                    f = form.cleaned_data
                    submitted = "an event or meeting"
                    body = """
                    Start date: {}\n
                    End date: {}\n
                    Title: {}|\n
                    Location: {}\n
                    Description: {}\n
                    URL: {}
                    """.format(
                        f["start_date"],
                        f["end_date"],
                        f["title"],
                        f["location"],
                        f["description"],
                        f["url"],
                    )
            if "submit_funding" in request.POST:
                form = FundingResourceForm(request.POST)
                if form.is_valid():
                    f = form.cleaned_data
                    submitted = "a funding resource"
                    body = """
                    Name: {}\n
                    URL: {}\n
                    Due Date: {}\n
                    Description: {}\n
                    Source: {}\n
                    """.format(
                        f["name"], f["url"], f["due_date"], f["description"], f["source_name"]
                    )
            if "submit_technical" in request.POST:
                form = TechnicalResourceForm(request.POST)
                if form.is_valid():
                    f = form.cleaned_data
                    submitted = "a technical resource"
                    body = """
                    Name: {}\n
                    URL: {}\n
                    Summary: {}\n
                    Publication Date: {}\n
                    Source: {}\n
                    """.format(
                        f["name"], f["url"], f["summary"], f["publication_date"], f["source"]
                    )

            # create the message from various fields
            message = "{} ({}) submitted {} at centraljerseytf.org:\n {}".format(
                f["your_name"], f["email"], submitted, textwrap.dedent(body)
            )
            send_mail(
                "Submitted contact form from CJTF website",
                message,
                "contact@centraljerseytf.org",
                ["kwarner@dvrpc.org"],
            )

            return HttpResponseRedirect("/thanks")
    form = TypeContactForm(label_suffix="")
    page = get_object_or_404(Page, internal_name="contact")
    context = {
        "title": page.title,
        "page": page,
        "first_form": True,
        "form": form,
    }
    return render(request, "web/contact.html", context)


def thanks(request):
    return render(request, "web/thankyou.html")


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

from django.utils.html import format_html

import django_tables2 as tables

from .models import TechnicalResource, FundingResource


class TechnicalResourceTable(tables.Table):
    class Meta:
        model = TechnicalResource
        fields = ("name", "publication_date", "source", "summary", "category")
        attrs = {"class": "responsive_table resources"}

    # data-th attribute for responsive mode
    name = tables.Column(attrs={"td": {"data-th": "Publication Name"}})
    publication_date = tables.Column(attrs={"td": {"data-th": "Publication Date"}})
    source = tables.Column(attrs={"td": {"data-th": "Source"}})
    summary = tables.Column(attrs={"td": {"data-th": "Summary"}})
    category = tables.Column(attrs={"td": {"data-th": "Category"}})

    def render_name(self, value, record):
        if record.pdf:
            return format_html("<a href='../files/{}' target='new'>{}</a>", record.pdf, value)
        if record.url:
            return format_html("<a href='{}' target='new'>{}</a>", record.url, value)


class FundingResourceTable(tables.Table):
    class Meta:
        model = FundingResource
        fields = ("name", "due_date", "source_name", "description")
        attrs = {"class": "responsive_table resources"}

    # data-th attribute for responsive mode
    name = tables.Column(attrs={"td": {"data-th": "Program Name"}})
    due_date = tables.Column(attrs={"td": {"data-th": "Due Date"}})
    source_name = tables.Column(attrs={"td": {"data-th": "Source"}})
    description = tables.Column(attrs={"td": {"data-th": "Description"}})

    def render_name(self, value, record):
        if record.url:
            return format_html("<a href={}>{}</a>", record.url, value)

from django.utils.html import format_html

import django_tables2 as tables

from .models import TechnicalResource, FundingResource


class TechnicalResourceTable(tables.Table):
    class Meta:
        model = TechnicalResource
        fields = ("name", "publication_date", "source", "summary", "category", "mpo")
        attrs = {"class": "responsive_table resources"}

    # data-th attribute for responsive mode
    # also disable ordering for summary
    name = tables.Column(attrs={"td": {"data-th": "Publication Name"}})
    publication_date = tables.Column(attrs={"td": {"data-th": "Publication Date"}})
    source = tables.Column(attrs={"td": {"data-th": "Source"}})
    summary = tables.Column(attrs={"td": {"data-th": "Summary"}}, orderable=False)
    category = tables.Column(attrs={"td": {"data-th": "Category"}})
    mpo = tables.Column(attrs={"td": {"data-th": "MPO Covered"}})

    def render_name(self, value, record):
        if record.pdf:
            return format_html("<a href='../files/{}' target='new'>{}</a>", record.pdf, value)
        if record.url:
            return format_html("<a href='{}' target='new'>{}</a>", record.url, value)

    def render_mpo(self, value, record):
        # List to string. We get the mpo value (not the lable) here, so make it uppercase.
        if record.mpo:
            mpo_string = ", ".join(record.mpo)
            return format_html(f"{mpo_string.upper()}")


class FundingResourceTable(tables.Table):
    class Meta:
        model = FundingResource
        fields = ("name", "due_date", "source_name", "description")
        attrs = {"class": "responsive_table resources"}

    # data-th attribute for responsive mode
    name = tables.Column(attrs={"td": {"data-th": "Program Name"}})
    due_date = tables.Column(attrs={"td": {"data-th": "Due Date"}})
    source_name = tables.Column(attrs={"td": {"data-th": "Source"}})
    description = tables.Column(attrs={"td": {"data-th": "Description"}}, orderable=False)

    def render_name(self, value, record):
        if record.url:
            return format_html("<a href={}>{}</a>", record.url, value)

import datetime

from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField

from ckeditor.fields import RichTextField


def validate_date_not_past(value):
    if value < datetime.date.today():
        raise ValidationError(
            "%(value)s is in the past.",
            params={"value": value},
        )


def default_mpo():
    return ["dvrpc", "njtpa"]


class ModifiedArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
            "widget": forms.CheckboxSelectMultiple,
            **kwargs,
        }
        return super(ArrayField, self).formfield(**defaults)


class Meeting(models.Model):
    date = models.DateTimeField(
        help_text=(
            "Date in format m/d/yyyy, m/d/yy, yy-m-d, or yyyy-m-d  and "
            "time in 24 hr format, i.e. 09:00 for 9am or 13:00 for 1pm"
        )
    )
    url = models.URLField(blank=True, null=True, help_text="To the Ticketleap page.")
    agenda = models.FileField(blank=True, null=True)
    minutes = models.FileField(blank=True, null=True)
    minutes_added = models.DateField(blank=True, null=True)
    presentation_materials = models.FileField(blank=True, null=True)
    pre_mat_added = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.date.strftime("%Y - %B"))

    def simplified_date(self):
        return str(self.date.strftime("%Y - %B"))

    def has_agenda(self):
        return bool(self.agenda)

    def has_minutes(self):
        return bool(self.minutes)

    def has_presentation_materials(self):
        return bool(self.presentation_materials)

    simplified_date.admin_order_field = "date"
    simplified_date.short_description = "date"  # so col heading is not "SIMPLIFIED DATE"
    has_agenda.boolean = True
    has_minutes.boolean = True
    has_presentation_materials.boolean = True


class Event(models.Model):
    start_date = models.DateField(validators=[validate_date_not_past])
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=200, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.title

    def display_date(self):
        date = (
            datetime.datetime.strftime(self.start_date, "%B %d, %Y").lstrip("0").replace(" 0", " ")
        )
        if self.start_time:
            date += ",  " + datetime.time.strftime(self.start_time, "%I:%M %p").lstrip("0").replace(
                " 0", " "
            )

        if self.end_date:
            if self.start_date == self.end_date:
                if self.end_time:
                    date += " - " + datetime.time.strftime(self.end_time, "%I:%M %p").lstrip(
                        "0"
                    ).replace(" 0", " ")
            else:
                if self.end_time:
                    date += " - " + datetime.datetime.strftime(self.end_date, "%B %d, %Y").lstrip(
                        "0"
                    ).replace(" 0", " ")
                    date += ", " + datetime.time.strftime(self.end_time, "%I:%M %p").lstrip(
                        "0"
                    ).replace(" 0", " ")
                else:
                    date += " - " + datetime.datetime.strftime(self.end_date, "%B %d, %Y").lstrip(
                        "0"
                    ).replace(" 0", " ")

        return date


class Page(models.Model):
    title = models.CharField(max_length=30, help_text="Title of the page.")
    main_content = RichTextField(help_text="Main content (left column).")
    sidebar = RichTextField(
        blank=True, null=True, help_text="Sidebar/additional info (right column)."
    )
    internal_name = models.CharField(
        max_length=30,
        help_text=(
            "Only editable by superuser; used to select appropriate page for views/templates."
        ),
    )

    def __str__(self):
        return self.title


class TechnicalResource(models.Model):
    category_choices = [
        ("regional_plans", "Regional Plans"),
        ("municipal_tools", "Municipal Tools"),
        ("research_and_reports", "Research and Reports"),
    ]
    mpo_choices = (("dvrpc", "DVRPC"), ("njtpa", "NJTPA"))
    name = models.CharField(max_length=200, verbose_name="Product Name")
    url = models.URLField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    mpo = ModifiedArrayField(
        models.CharField(choices=mpo_choices, max_length=5),
        default=default_mpo,
        verbose_name="MPO Covered",
    )
    publication_date = models.DateField(verbose_name="Publication Date")
    source = models.CharField(max_length=100)
    category = models.CharField(
        max_length=30,
        choices=category_choices,
    )
    pdf = models.FileField(blank=True)

    def __str__(self):
        return self.name


class FundingResource(models.Model):
    name = models.CharField(max_length=200, verbose_name="Program Name")
    url = models.URLField()
    due_date = models.DateField(blank=True, null=True, verbose_name="Due Date")
    source_name = models.CharField(max_length=200, verbose_name="Source")
    description = models.TextField(blank=True, null=True)
    pdf = models.FileField(blank=True)

    def __str__(self):
        return self.name


class FileUpload(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField()

    def __str__(self):
        return self.name

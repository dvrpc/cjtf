import datetime

from django.db import models

from ckeditor.fields import RichTextField


class Meeting(models.Model):
    date = models.DateTimeField(
        help_text=(
            "Date in format m/d/yyyy, m/d/yy, yy-m-d, or yyyy-m-d  and "
            "time in 24 hr format, i.e. 09:00 for 9am or 13:00 for 1pm"
        )
    )
    url = models.URLField(
        blank=True,
        null=True,
        help_text="To the Ticketleap page. Include the full url, i.e. start with http://",
    )
    agenda = models.FileField(blank=True, null=True)
    minutes = models.FileField(blank=True, null=True)
    minutes_added = models.DateField(blank=True, null=True)
    presentation_materials = models.FileField(blank=True)
    pre_mat_added = models.DateField(blank=True, null=True)

    def __str__(self):
        return str(self.date.strftime("%Y - %B"))

    def save(self, *args, **kwargs):
        if self.minutes:
            self.minutes_added = datetime.date.today()
        if self.presentation_materials:
            self.pre_mat_added = datetime.date.today()
        super().save(*args, **kwargs)

    def simplified_date(self):
        return str(self.date.strftime("%Y - %B"))

    def has_minutes(self):
        if self.minutes:
            return True
        else:
            return False

    def has_presentation_materials(self):
        if self.presentation_materials:
            return True
        else:
            return False

    simplified_date.admin_order_field = "date"
    simplified_date.short_description = "date"  # so col heading is not "SIMPLIFIED DATE"
    has_minutes.boolean = True
    has_presentation_materials.boolean = True


class Event(models.Model):
    date = models.DateTimeField(
        help_text=(
            "Date in format m/d/yyyy, m/d/yy, yy-m-d, or yyyy-m-d  and "
            "time in 24 hr format, i.e. 09:00 for 9am or 13:00 for 1pm"
        )
    )
    title = models.CharField(max_length=100)
    location = RichTextField(null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.title


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
    name = models.CharField(max_length=200)
    url = models.URLField(blank=True, null=True, help_text="Be sure to include http:// or https://")
    summary = models.TextField(blank=True, null=True)
    publication_date = models.DateField()
    source = models.CharField(max_length=100)
    category = models.CharField(max_length=30, choices=category_choices,)
    pdf = models.FileField(blank=True)

    def __str__(self):
        return self.name


class FundingResource(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(help_text="Include http://")
    due_date = models.DateField(blank=True, null=True)
    source_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    pdf = models.FileField(blank=True)

    def __str__(self):
        return self.name


class FileUpload(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField()

    def __str__(self):
        return self.name

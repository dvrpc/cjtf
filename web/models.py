from django.db import models

from ckeditor.fields import RichTextField


class Event(models.Model):
    date = models.DateTimeField()
    location = models.TextField(max_length=200)
    title = models.CharField(max_length=100)
    agenda = RichTextField()
    minutes = models.FileField(blank=True)
    presentation_materials = models.FileField(blank=True)

    def __str__(self):
        return self.title

class Page(models.Model):
    title = models.CharField(max_length=30, help_text="Title of the page.")
    main_content = RichTextField(help_text="Main content (left column).")
    sidebar = RichTextField(blank=True, null=True, help_text="Sidebar/additional info (right column).")
    internal_name = models.CharField(max_length=30, help_text="Do not change!")

    def __str__(self):
        return self.title

class TechnicalResource(models.Model):
    category_choices = [
        ("RP", "Regional Plans"),
        ("MT", "Municipal Tools"),
        ("RR", "Research and Reports"),
    ]
    name = models.CharField(max_length=200)
    url = models.URLField()
    summary = models.TextField()
    publication_date = models.DateField()
    source = models.CharField(max_length=100)
    category = models.CharField(
        max_length=2,
        choices=category_choices,
    )
    pdf = models.FileField(blank=True)

    def __str__(self):
        return self.name

class FundingResource(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    due_date = models.DateField()
    source_name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name


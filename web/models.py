from django.db import models

from ckeditor.fields import RichTextField


class Event(models.Model):
    date = models.DateTimeField()
    location = models.CharField(max_length=500)
    title = models.CharField(max_length=200)
    agenda = RichTextField()
    minutes = models.FileField(blank=True)
    presentation_materials = models.FileField(blank=True)

    def __str__(self):
        return self.title


class Page(models.Model):
    title = models.CharField(max_length=30, help_text="Title of the page.")
    main_content = RichTextField(help_text="Main content (left column).")
    sidebar = RichTextField(help_text="Sidebar/additional info (right column).")
    internal_name = models.CharField(max_length=30, help_text="Do not change!")

    def __str__(self):
        return self.title

# Resources
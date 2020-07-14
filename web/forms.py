import datetime

from django import forms
from django.core.exceptions import ValidationError

from .models import FundingResource, TechnicalResource, Event


class TypeContactForm(forms.Form):
    type_of_contact = forms.ChoiceField(
        choices=[
            ("comment_or_question", "Comment or Question"),
            ("event", "Meeting or Event"),
            ("funding_resource", "Funding Resource"),
            ("technical_resource", "Technical Resource"),
        ],
        label="I would like to submit a ",
    )
    type_of_contact.widget.attrs.update({"class": "bigger form_buttons"})


class CommentForm(forms.Form):
    required_css_class = "required"
    comment = forms.CharField(max_length=1000, widget=forms.Textarea)
    your_name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(max_length=100)


class EventForm(forms.ModelForm):
    required_css_class = "required"
    your_name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(max_length=100)

    class Meta:
        model = Event
        fields = [
            "start_date",
            "title",
            "location",
            "description",
            "url",
        ]
        labels = {
            "start_date": "Date",
            "url": "URL",
        }
        help_texts = {
            "start_date": "mm/dd/yy",
        }

    def clean_start_date(self):
        data = self.cleaned_data["start_date"]
        if data < datetime.date.today():
            raise ValidationError("Invalid date - date cannot be in the past.")
        return data


class TechnicalResourceForm(forms.ModelForm):
    required_css_class = "required"
    your_name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(max_length=100)

    class Meta:
        model = TechnicalResource
        fields = ["name", "url", "summary", "publication_date", "source"]
        labels = {"url": "URL"}

    def clean_publication_date(self):
        data = self.cleaned_data["publication_date"]
        if data > datetime.date.today():
            raise ValidationError("Invalid date - date cannot be in the future.")
        return data


class FundingResourceForm(forms.ModelForm):
    required_css_class = "required"
    your_name = forms.CharField(max_length=100, label="Your Name")
    email = forms.EmailField(max_length=100)

    class Meta:
        model = FundingResource
        fields = ["name", "url", "due_date", "source_name", "description"]
        labels = {"url": "URL"}

    def clean_due_date(self):
        data = self.cleaned_data["due_date"]
        if data < datetime.date.today():
            raise ValidationError("Invalid date - date cannot be in the past.")
        return data

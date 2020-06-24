from django import forms

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
    type_of_contact.widget.attrs.update({"class": "bigger"})


class CommentForm(forms.Form):
    your_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)
    comment = forms.CharField(max_length=1000, widget=forms.Textarea)


class EventForm(forms.ModelForm):
    your_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = Event
        fields = [
            "start_date",
            "end_date",
            "title",
            "location",
            "description",
            "url",
        ]


class TechnicalResourceForm(forms.ModelForm):
    your_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = TechnicalResource
        fields = ["name", "url", "summary", "publication_date", "source"]


class FundingResourceForm(forms.ModelForm):
    your_name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)

    class Meta:
        model = FundingResource
        fields = ["name", "url", "due_date", "source_name", "description"]

from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Event


class UserCreationFormWithName(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'password1', 'password2', )

    def save(self, commit=True):
        user = super(UserCreationFormWithName, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        if commit:
            user.save()
        return user

      
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'image_url', 'event_date', 'event_time']

    def clean_event_date(self):
        date = self.cleaned_data['event_date']
        if date < date.today():
            raise forms.ValidationError("The event date cannot be in the past.")
        return date

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if not name:
            raise forms.ValidationError("The event name cannot be blank.")
        return name

    def clean_description(self):
        description = self.cleaned_data['description'].strip()
        if len(description) < 10:
            raise forms.ValidationError("The description is too short. Please provide more details.")
        return description
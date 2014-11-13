from django import forms
from atlas.models import Greeting
from atlas.models import Story

class CreateGreetingForm(forms.ModelForm):
    class Meta:
        model = Greeting
        exclude = ['author', 'date']

class CreateStoryForm(forms.ModelForm):
    class Meta:
        model = Story
        title = forms.CharField()
        content = forms.CharField(widget=forms.Textarea)
        timeToWrite = forms.CharField(widget=forms.HiddenInput())
        exclude = ['authorID','url', 'pages', 'authorName','wordMemory','relatedImages']

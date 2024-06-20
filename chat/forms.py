from django.forms import ModelForm
from django import forms
from .models import Message, UserMessage
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'attachment']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type a message...'}),
        }

    attachment = forms.FileField(required=False)


class UserMessageForm(forms.ModelForm):
    class Meta:
        model = UserMessage
        fields = ['text', 'attachment']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Type a message...'}),
        }

    attachment = forms.FileField(required=False)


class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
from django.forms import ModelForm
from django import forms
from .models import *

class ChatMessageCreateForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Type your message here...', 'class': 'p-4 text-black', 'maxlength': 500, 'autofocus': True})
        }

class NewGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
            'groupchat_name': forms.TextInput(attrs={
                'placeholder': 'Add Name...',
                'class': 'p-4 text-black',
                'maxlength':'300',
                'autofocus': True

            }),
        }
class ChatRoomEditForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['groupchat_name']
        widgets = {
           'groupchat_name': forms.TextInput(attrs={
                'class': 'p-4 text-xl font-bold  mb-4',
                'maxlength':'300',}),
        }

class EditMessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Edit your message here...', 'class': 'p-4 text-black', 'maxlength': 500, 'autofocus': True})
        }
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Required. Max 50 characters. Letters, digits and @/./+/-/_ only.'
        self.fields['password1'].help_text = "Required. Alphanumeric. At least one letter. Not similar to other information."





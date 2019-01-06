from django import forms
from django.contrib.auth.models import User
import re


class SignUpForm(forms.ModelForm):

    username = forms.CharField(
        label="Username:",
        strip=False,
        widget=forms.TextInput,
        help_text="Minimum 5 characters, only letters, digits and underscores allowed. Must start with a letter,"
                  "Can't end with an underscore. "
    )

    password1 = forms.CharField(
        label="Password:",
        strip=False,
        widget=forms.PasswordInput,
        help_text="Minimum 8 characters, at least one number."

    )

    password2 = forms.CharField(
        label="Repeat password:",
        strip=False,
        widget=forms.PasswordInput,
        help_text=""
    )

    class Meta:
        model = User
        fields = ['username']

    def clean_password2(self):
        p1 = self.cleaned_data.get("password1")
        p2 = self.cleaned_data.get("password2")
        if p1 and p1 != p2:
            raise forms.ValidationError("Passwords don't match.")
        if not any(c.isdigit() for c in p1):
            raise forms.ValidationError("Password must contain at least one digit.")
        if len(p1) < 8:
            raise forms.ValidationError("Password must have at least 8 characters")
        return p2

    def clean_username(self):
        un = self.cleaned_data.get("username")
        pattern = "^[A-Za-z][A-Za-z_0-9]*[a-zA-Z0-9]$"
        match = re.search(pattern, un)
        if not match:
            raise forms.ValidationError("Username doesn't meet the criteria.")
        if len(un) < 5:
            raise forms.ValidationError("Username is too short.")
        return un

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

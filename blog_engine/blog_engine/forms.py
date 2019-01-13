import re

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

username_field = username = forms.CharField(
    label="Username:",
    strip=False,
    widget=forms.TextInput,
    help_text="Minimum 5 characters, only letters, digits and underscores allowed. Must start with a letter,"
              "Can't end with an underscore. "
)


def validate_password(self, input1, input2):
    p1 = self.cleaned_data.get(input1)
    p2 = self.cleaned_data.get(input2)
    if p1 and p1 != p2:
        raise forms.ValidationError("Passwords don't match.")
    if not any(c.isdigit() for c in p1):
        raise forms.ValidationError("Password must contain at least one digit.")
    if len(p1) < 8:
        raise forms.ValidationError("Password must have at least 8 characters")
    return p2


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
        validate_password(self, "password1", "password2")

    def clean_username(self):
        un = self.cleaned_data.get("username")
        pattern = "[A-Za-z][A-Za-z_0-9]*[a-zA-Z0-9]"
        match = re.fullmatch(pattern, un)
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


class ChangePasswordForm(forms.Form):
    oldpassword = forms.CharField(
        label="Old password:",
        strip=False,
        widget=forms.PasswordInput
    )

    newpassword1 = forms.CharField(
        label="New password:",
        strip=False,
        widget=forms.PasswordInput
    )

    newpassword2 = forms.CharField(
        label="Repeat new password",
        strip=False,
        widget=forms.PasswordInput
    )

    def clean_oldpassword(self):
        pw = self.cleaned_data.get("oldpassword")
        user = authenticate(username=self.user.username, password=pw)
        if not user:
            raise forms.ValidationError("The old password is incorrect.")
        return pw

    def clean_newpassword2(self):
        validate_password(self, "newpassword1", "newpassword2")

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")
        super().__init__(*args, **kwargs)


class ChangeUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

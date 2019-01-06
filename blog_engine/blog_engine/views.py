from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth.forms import UserCreationForm


def index(request):
    return render(request, "index/index.html")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "registration/registration_successful.html")
        else:
            return render(request, "registration/register.html", {'form': form})

    else:
        form = SignUpForm()
        return render(request, "registration/register.html", {'form': form})




from django.shortcuts import render


def index(request):
    return render(request, "anonymous_index.html")


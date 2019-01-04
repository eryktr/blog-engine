from django.shortcuts import render


def index(request):
    return render(request, "index/anonymous_index.html")


def mod(request):
    return render(request, "index/mod_index.html")


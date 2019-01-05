from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        return render(request, "index/admin_index.html")
    return render(request, "index/anonymous_index.html")



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import NewPostForm


@login_required()
def new_post(request):
    template_name = "content/new_post.html"
    if request.method == "POST":
        form = NewPostForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            return render(request, template_name, {'form': form})
    else:
        user = request.user
        form = NewPostForm(user)
        return render(request, template_name, {'form': form})

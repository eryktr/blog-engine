from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect
from .forms import NewPostForm
from .models import Post

no_permission_template = "shared/no_permission.html"


@login_required()
def new_post(request):
    if not request.user.has_perm('content.add_post'):
        return render(request, no_permission_template)
    template_name = "content/new_post.html"
    if request.method == "POST":
        form = NewPostForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            form.save_m2m()
            return redirect("index")
        else:
            return render(request, template_name, {'form': form})
    else:
        user = request.user
        form = NewPostForm(user)
        return render(request, template_name, {'form': form})


@login_required()
def delete_post(request, post_id):
    post = Post.objects.filter(id=post_id)

    if not post.exists() or not (request.user.has_perm("content.delete_post") or request.user == post.author):
        return render(request, no_permission_template)
    post.delete()
    return redirect("index")


def view_post(request, post_id):
    post = Post.objects.filter(id=post_id)
    if not post.exists():
        return render(request, no_permission_template)
    post = Post.objects.get(id=post_id)
    return render(request, "content/view_post.html", {'post': post})


@login_required()
def edit_post(request, post_id):
    post = Post.objects.get(id=post_id)
    if not (request.user.has_perm("content.edit_post") or request.user == post.author):
        return render(request, no_permission_template)
    if request.method == "POST":
        form = NewPostForm(request.user, request.POST, instance=post)
        if form.is_valid():
            form.save()
            form.save_m2m()
            return redirect("index")
        else:
            return render(request, "content/edit_post.html", {'form': form})

    else:
        form = NewPostForm(request.user, instance=post)
        return render(request, "content/edit_post.html", {'form': form})

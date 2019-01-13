from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404

from .forms import NewPostForm, EditPostForm
from .models import Post


@login_required()
@permission_required('content.add_post', raise_exception=True)
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


@login_required()
def delete_post(request, post_id):
    if request.method != "POST":
        raise PermissionDenied
    post = get_object_or_404(Post, id=post_id)

    if not (request.user.has_perm("content.delete_post") or request.user == post.author):
        raise PermissionDenied
    post.delete()
    return redirect("index")


def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "content/view_post.html", {'post': post})


@login_required()
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if not (request.user.has_perm("content.change_post") or request.user == post.author):
        raise PermissionDenied
    if request.method == "POST":
        form = EditPostForm(post.author, request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect("index")
        else:
            return render(request, "content/edit_post.html", {'form': form})
    else:
        form = EditPostForm(post.author, instance=post)
        return render(request, "content/edit_post.html", {'form': form})

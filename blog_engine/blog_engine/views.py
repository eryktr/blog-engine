from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordContextMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, ListView
from .forms import SignUpForm, ChangePasswordForm, ChangeUserForm
try:
    from ..content.models import Post, Tag
except ValueError:
    from content.models import Post, Tag


class PostsView(ListView):
    template_name = "index/index.html"
    context_object_name = "posts"
    ordering = ["-post_date"]
    paginate_by = 2

    def get_queryset(self):
        new_queryset = Post.objects
        filter_tag = self.request.GET.getlist('filter_tag', None)
        filter_tag_any = self.request.GET.get("filter_tag")
        if filter_tag_any is not None:
            new_queryset = Post.objects.filter(tags__name__in=filter_tag)
        order = self.request.GET.get('orderby', "none")
        new_queryset = new_queryset.order_by("-post_date")
        if order != "none":
            new_queryset = new_queryset.order_by(order)
        return new_queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orderby'] = self.request.GET.get('orderby')
        context['orderings'] = [
            ("none", "None"),
            ("title", "Title asc"),
            ("-title", "Title desc"),
            ("author", "Author asc"),
            ("-author", "Author desc"),
        ]
        context["tags"] = Tag.objects.values("name")
        context["tag_filters"] = self.request.GET.getlist("filter_tag")
        return context


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


class PasswordChangeView(PasswordContextMixin, FormView):
    form_class = ChangePasswordForm
    template_name = "registration/password_change_form.html"
    success_url = reverse_lazy('password_change_done')
    title = "Password change"

    @method_decorator(sensitive_post_parameters())
    @method_decorator(csrf_protect)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        pw = form.cleaned_data.get("newpassword1")
        self.request.user.set_password(pw)


@login_required()
def show_profile(request):
    user = request.user
    if request.method == 'POST':
        form = ChangeUserForm(request.POST, instance=user)
        if form.is_valid:
            form.save()
            return redirect("index")
        else:
            return render(request, "profile/show_profile.html", {'form': form})
    else:
        form = ChangeUserForm(initial={'email': user.email, 'first_name': user.first_name, 'last_name': user.last_name},
                              instance=user)
        return render(request, "profile/show_profile.html", {'form': form})

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordContextMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView
from .forms import SignUpForm, ChangePasswordForm, ChangeUserForm
from content.models import Post


def index(request):
    posts = Post.objects.all()
    return render(request, "index/index.html", {'posts': posts})


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

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from .forms import RegistrationForm


class SignUp(FormView):
    template_name = "signup.html"
    form_class = RegistrationForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email = form.cleaned_data["email"]
        user.set_password(form.cleaned_data["password"])
        user.save()
        return HttpResponseRedirect(self.success_url)

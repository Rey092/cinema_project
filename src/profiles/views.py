from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import UpdateView

from .forms import UserProfileForm


class UserProfileFormView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfileForm
    template_name = 'profiles/pages/user_profile.html'
    form_class = UserProfileForm
    success_message = 'Success'

    def get_success_url(self):
        return reverse('user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        new_password = form.cleaned_data.get('new_password')
        confirm_password = form.cleaned_data.get('confirm_password')

        if new_password == confirm_password and new_password:
            self.request.user.set_password(new_password)
            self.request.user.save()
            return redirect(reverse('admin_lte_home'))

        return super().form_valid(form)

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import UpdateView

from .forms import UserProfileForm, UserProfileRegistrationForm
from .models import UserProfile


class UserProfileFormView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    template_name = 'profiles/pages/user_profile.html'
    form_class = UserProfileForm
    success_message = 'Success'
    login_url = '/login/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_success_url(self):
        return reverse('profiles:user_profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        new_password = form.cleaned_data.get('new_password')
        confirm_password = form.cleaned_data.get('confirm_password')

        if new_password == confirm_password and new_password:
            self.request.user.set_password(new_password)
            self.request.user.save()
            return reverse('profiles:user_profile')

        return super().form_valid(form)


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('cinema_site:home_page')

    form = UserProfileRegistrationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        # TODO: Email confirmation
        # subject = 'Please Activate Your Account'
        # current_site = get_current_site(request)
        # message = render_to_string('profiles/messages/activation_request.html', {
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        #     'token': account_activation_token.make_token(user),
        # })
        # user.email_user(subject, message)
        return redirect('cinema_site:home_page')

    return render(request, 'profiles/pages/signup.html', {'form': form})

# TODO: Email confirmation
# def activation_sent_view(request):
#     return render(request, 'profiles/messages/activation_sent.html')

# TODO: Email confirmation
# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = UserProfile.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
#         user = None
#
#     if user is not None and account_activation_token.check_token(user, token):
#         user.is_active = True
#         user.save()
#         login(request, user)
#         return redirect('cinema_site:home_page')
#     else:
#         return render(request, 'profiles/messages/activation_invalid.html')

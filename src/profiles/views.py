from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import UpdateView, CreateView

from .forms import UserProfileForm, UserProfileRegistrationForm
from .models import UserProfile
from .tokens import account_activation_token


class UserProfileFormView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserProfile
    template_name = 'profiles/pages/user_profile.html'
    form_class = UserProfileForm
    success_message = 'Success'

    def get_initial(self):
        self.initial.update({'created_by': self.request.user})
        return self.initial

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
            return redirect(reverse('admin_lte:admin_lte_home'))

        return super().form_valid(form)


# class UserProfileSignUpView(CreateView):
#     model = UserProfile
#     form_class = UserProfileRegistrationForm
#     template_name = 'profiles/pages/sign_up.html'
#     success_url = reverse_lazy('cinema_site:home_page')


def signup_view(request):
    if request.method == 'POST':
        pass
        form = UserProfileRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            # user.profile.first_name = form.cleaned_data.get('first_name')
            # user.profile.last_name = form.cleaned_data.get('last_name')
            # user.profile.email = form.cleaned_data.get('email')
            # user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Please Activate Your Account'
            message = render_to_string('profiles/messages/activation_request.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('profiles:activation_sent')
    else:
        form = UserProfileRegistrationForm()
    return render(request, 'profiles/pages/signup.html', {'form': form})


def activation_sent_view(request):
    return render(request, 'profiles/pages/activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = UserProfile.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('cinema_site:home_page')
    else:
        return render(request, 'profiles/pages/templates/profiles/messages/activation_invalid.html')

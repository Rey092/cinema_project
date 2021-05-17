from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import CharField, DateInput, EmailInput, ModelForm, PasswordInput, Select, TextInput

from .models import UserProfile


class UserProfileForm(LoginRequiredMixin, ModelForm):
    form_class = PasswordChangeForm
    new_password = CharField(
        widget=PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль'}),
        label='Новый пароль', required=False)
    confirm_password = CharField(
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль', }),
        label='Повторите пароль', required=False)

    class Meta:
        model = UserProfile
        form_class = PasswordChangeForm
        fields = ['first_name', 'language', 'last_name', 'gender', 'username', 'phone_number',
                  'email', 'birthday', 'address', 'city', 'cc_number']
        widgets = {
            'first_name': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Input text',
            }),
            'language': Select(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Выберите язык',
                'label': 'Язык'
            }),
            'last_name': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Input text',
            }),
            'gender': Select(attrs={
                'required': 'required',
                'class': 'form-control',
            }),
            'username': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Input username',
            }),
            'phone_number': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите номер телефона',
            }),
            'email': EmailInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Short description',
            }),
            'birthday': DateInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Input text',
            }),
            'address': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Input text',
            }),
            'city': Select(attrs={
                'required': 'required',
                'class': 'form-control',
            }),
            'cc_number': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Input text',
            }),
        }

    field_order = ['first_name', 'language', 'last_name', 'gender', 'username', 'phone_number',
                   'email', 'birthday', 'address', 'city', 'new_password', 'confirm_password', 'cc_number']

    def clean(self):
        cd = self.cleaned_data
        if cd.get('new_password') != cd.get('confirm_password'):
            self.add_error('confirm_password', 'passwords do not match !')
        return cd

    # def __int__(self):
    #     self.fields['new_password'].required = False
    #     self.fields['confirm_password'].required = False

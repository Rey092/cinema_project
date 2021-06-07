from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import CharField, DateInput, EmailInput, ModelForm, PasswordInput, Select, TextInput

from .models import UserProfile


class UserProfileForm(LoginRequiredMixin, ModelForm):
    new_password = CharField(
        widget=PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль', 'autocomplete': 'off'}),
        label='Новый пароль', required=False)
    confirm_password = CharField(
        widget=PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль', 'autocomplete': 'off'}),
        label='Повторите пароль', required=False)

    def __init__(self, *args, **kwargs):
        self.created_by = kwargs['initial']['created_by']
        super().__init__(*args, **kwargs)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'language', 'last_name', 'gender', 'username', 'phone_number',
                  'email', 'birthday', 'address', 'city', 'cc_number']
        widgets = {
            'first_name': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите имя',
                'label': 'Имя'
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
                'placeholder': 'Введите фамилию',
                'label': 'Фамилия'
            }),
            'gender': Select(attrs={
                'required': 'required',
                'class': 'form-control',
            }),
            'username': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите никнейм',
                'label': 'Никнейм'
            }),
            'phone_number': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите номер телефона',
                'label': 'Номер телефона'
            }),
            'email': EmailInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите электронный адрес',
                'label': 'E-mail'
            }),
            'birthday': DateInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите дату рождения',
                'label': 'Дата рождения'
            }),
            'address': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите адрес',
                'label': 'Адрес'
            }),
            'city': Select(attrs={
                'required': 'required',
                'class': 'form-control',
                'label': 'Город'
            }),
            'cc_number': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер карты',
                'label': 'Карта'
            }),
        }

    field_order = ['first_name', 'language', 'last_name', 'gender', 'username', 'phone_number',
                   'email', 'birthday', 'address', 'city', 'new_password', 'confirm_password', 'cc_number']

    def clean(self):
        clean_data: dict = super().clean()
        if clean_data['new_password'] != clean_data['confirm_password']:
            self.add_error('confirm_password', 'Пароли не сходятся !')
            self.add_error('new_password', 'Пароли не сходятся !')
        return clean_data

    def clean_email(self):
        old_email = self.created_by.email
        new_email = self.cleaned_data.get('email')

        if new_email != old_email:
            if UserProfile.objects.filter(email__iexact=new_email).exists():
                self.add_error('email', 'Этот email уже существует !')

        return new_email


class UserProfileFormRestricted(ModelForm):
    class Meta(UserProfileForm.Meta):
        model = UserProfile


class UserProfileRegistrationForm(UserCreationForm):
    password1 = CharField(
        widget=PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль', 'autocomplete': 'off'}),
        label='Новый пароль',
        help_text=password_validation.password_validators_help_text_html(),
        required=False, strip=False, )
    password2 = CharField(
        widget=PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Повторите пароль', 'autocomplete': 'off'}),
        label='Повторите пароль',
        help_text=password_validation.password_validators_help_text_html(),
        required=False, strip=False, )

    class Meta(UserProfileForm.Meta):
        model = UserProfile
        exclude = ['cc_number', ]
        # fields = UserProfileForm.Meta.fields + ['password1', 'password2', ]
        # widgets = UserProfileForm.Meta.widgets
        # widgets.update({
        #     'password1': PasswordInput(attrs={
        #         'required': 'required',
        #         'class': 'form-control',
        #         'placeholder': 'Введите новый пароль',
        #         'label': 'Пароль'
        #     }),
        #     'password2': PasswordInput(attrs={
        #         'required': 'required',
        #         'class': 'form-control',
        #         'placeholder': 'Повторите пароль',
        #         'label': 'Пароль снова'
        #     }),
        # })
    # def clean(self):
    #     clean_data: dict = super().clean()
    #     if clean_data['new_password'] != clean_data['confirm_password']:
    #         self.add_error('confirm_password', 'Пароли не сходятся !')
    #         self.add_error('new_password', 'Пароли не сходятся !')
    #     return clean_data
    #
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if UserProfile.objects.filter(email__iexact=email).exists():
    #         self.add_error('email', 'Этот email уже существует !')
    #
    # def save(self, commit=True):
    #     instance: UserProfile = super().save(commit=False)
    #     instance.is_active = False
    #
    #     instance.save()
    #     return instance

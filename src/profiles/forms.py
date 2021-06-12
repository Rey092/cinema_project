import datetime

from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.forms import CharField, DateInput, EmailInput, ModelForm, PasswordInput, Select, TextInput

from .models import UserProfile


class UserProfileForm(ModelForm):
    new_password = CharField(
        widget=PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Введите новый пароль', 'autocomplete': 'off'}),
        label='Новый пароль',
        help_text=password_validation.password_validators_help_text_html(),
        required=False, strip=False, )
    confirm_password = CharField(
        widget=PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Повторите пароль', 'autocomplete': 'off'}),
        label='Повторите пароль',
        help_text=password_validation.password_validators_help_text_html(),
        required=False, strip=False, )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
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
                'label': 'E-mail',
            }),
            'birthday': DateInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите дату рождения',
                'label': 'Дата рождения',
                'data-date-format': 'dd/mm//yyyy'
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

    def clean_username(self):
        old_username = self.user.username
        new_username = self.cleaned_data.get('username')

        if new_username != old_username:
            if UserProfile.objects.filter(username__iexact=new_username).exists():
                self.add_error('username', 'Имя пользователя должно быть уникальным !')

        symbols_list = ['@', '.', '-', '+', '_']
        if any(symbol in new_username for symbol in symbols_list):
            self.add_error('username', 'Символы @/./-/+/_ не разрешены для имени пользователя')

        return new_username

    def clean_email(self):
        old_email = self.user.email
        new_email = self.cleaned_data.get('email')

        if new_email != old_email:
            if UserProfile.objects.filter(email__iexact=new_email).exists():
                self.add_error('email', 'Email пользователя должен быть уникальным !')

        return new_email

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if not (datetime.date(1900, 1, 1) <= birthday <= datetime.date.today()):
            self.add_error('birthday', 'Введите корректную дату рождения с 1900 года до сегодня !')
        return birthday


class UserProfileFormRestricted(ModelForm):
    class Meta(UserProfileForm.Meta):
        model = UserProfile

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# class UserProfileFormRestricted(ModelForm):
#     class Meta(UserProfileForm.Meta):
#         model = UserProfile


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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        symbols_list = ['@', '.', '-', '+', '_']
        if any(symbol in username for symbol in symbols_list):
            self.add_error('username', 'Символы @/./-/+/_ не разрешены для имени пользователя')
        return username

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if not (datetime.date(1900, 1, 1) <= birthday <= datetime.date.today()):
            self.add_error('birthday', 'Введите корректную дату рождения с 1900 года до сегодня !')
        return birthday

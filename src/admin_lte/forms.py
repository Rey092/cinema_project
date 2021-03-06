from cinema_site.models import Cinema, Hall, Image, Movie, SeoData, Article, Page, Contacts, EmailTemplate, \
    BackgroundImage
from django.core.exceptions import ValidationError
from django.forms import CheckboxInput, DateInput, FileInput, ModelForm, NumberInput, Textarea, TextInput, URLInput, \
    SlugField, ImageField, RadioSelect, ChoiceField, CharField


class ImageForm(ModelForm):
    # model = Image
    # fields = ['image', ]
    # labels = {
    #     'image': 'Картинка'
    # }

    class Meta:
        model = Image
        fields = ['image', ]


class BackgroundImageForm(ModelForm):
    class Meta:
        model = BackgroundImage
        fields = ['bg_format', 'image', 'top_banners_is_active']
        widgets = {
            'bg_format': RadioSelect(attrs={
                'required': 'required',
            }),
            'image': FileInput(attrs={
                'class': 'form-control',
            }),
            'top_banners_is_active': CheckboxInput(attrs={
                'name': 'switcher',
                'class': 'custom-control-input',
                'id': 'customSwitch3'
            })
        }


class SeoDataForm(ModelForm):
    class Meta:
        model = SeoData
        fields = ['title', 'url', 'keywords', 'description', 'seo_text']
        widgets = {
            'title': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите название для СЕО',
            }),
            'url': URLInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'URL',
            }),
            'keywords': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите СЕО ключевые слова',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите СЕО описание',
            }),
            'seo_text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите СЕО текст',
            }),
        }
        labels = {
            'title': 'СЕО - Заголовок',
            'url': 'СЕО - URL-адрес',
            'keywords': 'СЕО - Ключевые слова',
            'description': 'СЕО - Описание',
            'seo_text': 'СЕО - Текст',
        }


class MovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'slug', 'description', 'trailer_url', 'release_date', 'is_active',
                  'is_2d', 'is_3d', 'is_imax', 'poster']
        widgets = {
            'title': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите название фильма',
            }),
            'slug': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите slug-name',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание',
            }),
            'trailer_url': URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ссылку на трейлер',
            }),
            'release_date': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Выберите дату релиза',
            }),
            'is_active': CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customCheckbox4'
            }),
            'is_2d': CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'style': 'margin:15px',
                'id': 'customCheckbox1'
            }),
            'is_3d': CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'style': 'margin: 15px',
                'id': 'customCheckbox2'
            }),
            'is_imax': CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'style': 'margin:15px',
                'id': 'customCheckbox3'
            }),
            'poster': FileInput(),
        }
        labels = {
            'title': 'Название',
            'slug': 'Slug',
            'description': 'Описание',
            'trailer_url': 'Ссылка на трейлер',
            'release_date': 'Начало показов',
            'is_active': 'Активный',
            'is_2d': '2D',
            'is_3d': '3D',
            'is_imax': 'IMAX',
            'poster': 'Постер',
        }


class CinemaForm(ModelForm):
    class Meta:
        model = Cinema
        fields = ['name', 'slug', 'description', 'conditions', 'logo', 'banner']
        widgets = {
            'name': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите название фильма',
            }),
            'slug': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите slug-name',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание',
            }),
            'conditions': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите условия',
            }),
            'logo': FileInput(),
            'banner': FileInput(),
        }
        labels = {
            'name': 'Название кинотеатра',
            'slug': 'Slug',
            'description': 'Описание',
            'conditions': 'Условия',
            'logo': 'Лого',
            'banner': 'Баннер',
        }


class HallForm(ModelForm):
    class Meta:
        model = Hall
        fields = ['hall_number', 'description', 'conditions', 'layout', 'banner']
        widgets = {
            'hall_number': NumberInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите номер кинозала',
            }),
            'description': Textarea(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите описание',
            }),
            'conditions': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите условия',
            }),
            'layout': FileInput(),
            'banner': FileInput(),
        }
        labels = {
            'hall_number': 'Номер кинозала',
            'description': 'Описание',
            'conditions': 'Условия',
            'layout': 'Схема зала',
            'banner': 'Верхний баннер',
        }

    def validate_unique(self):
        exclude = self._get_validation_exclusions()
        exclude.remove('cinema')

        try:
            self.instance.validate_unique(exclude=exclude)
        except ValidationError as e:
            self._update_errors(e.message_dict)


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'description', 'trailer_url', 'is_active', 'publication', 'banner']
        widgets = {
            'title': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
            }),
            'slug': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите описание',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите условия',
            }),
            'trailer_url': URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ссылку на видео',
            }),
            'is_active': CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customCheckbox1'
            }),
            'publication': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Дата публикации',
            }),
            'banner': FileInput(),
        }
        labels = {
            'title': 'Заголовок',
            'slug': 'slug',
            'description': 'Описание',
            'video_url': 'Ссылка на видео',
            'is_active': 'Статус',
            'created': 'Дата публикации',
            'banner': 'Баннер'
        }


class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'slug', 'description', 'is_active', 'banner']
        widgets = {
            'title': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите название страницы',
            }),
            'slug': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите описание',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите условия',
            }),
            'is_active': CheckboxInput(attrs={
                'class': 'form-control custom-control-input',
                'id': 'customCheckbox1'
            }),
            'banner': FileInput(),
        }
        labels = {
            'title': 'Заголовок',
            'slug': 'slug',
            'description': 'Описание',
            'is_active': 'Статус',
            'banner': 'Баннер'
        }


class RestrictedPageForm(PageForm):
    class Meta(PageForm.Meta):
        exclude = ('title', 'slug', 'is_active')


class ContactsForm(ModelForm):
    class Meta:
        model = Contacts
        fields = ('name', 'address', 'coordinates', 'logo')

        widgets = {
            'name': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Введите название',
            }),
            'address': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес',
            }),
            'coordinates': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Введите координаты',
            }),
        }
        order = ['name', 'logo', 'address', 'coordinates']


class MailingForm(ModelForm):
    choice_types = (
        ('all', 'Все пользователи'),
        ('selected', 'Выборочно'),
    )
    users_choice_type = ChoiceField(choices=choice_types, widget=RadioSelect(), label='Выбрать пользователей:')
    text_field = CharField(widget=Textarea, label='Текст')

    def clean_users_choice_type(self):
        if len(self.cleaned_data['region']) > 1:
            raise ValidationError('Select only 1 option.')
        return self.cleaned_data['region']

    class Meta:
        model = EmailTemplate
        fields = ['file', ]
        labels = {
            'file': 'Загрузить HTML-письмо',
        }

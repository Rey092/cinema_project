from cinema_site.models import Cinema, CinemaGalleryImage, Image, Movie, MovieGalleryImage, SeoData
from django.forms import CheckboxInput, DateInput, FileInput, Form, ImageField, ModelForm, Textarea, TextInput, URLInput


class ImageForm(ModelForm):
    model = Image
    fields = ('image',)
    labels = {
        'image': 'Картинка'
    }


class MovieGalleryImageForm(ModelForm):
    class Meta:
        model = MovieGalleryImage
        fields = ('image',)
        labels = {
            'image': ''
        }


class CinemaGalleryImageForm(ModelForm):
    class Meta:
        model = CinemaGalleryImage
        fields = ('image',)
        labels = {
            'image': ''
        }


class PosterForm(Form):
    picture = ImageField(label='Новый постер:', required=False)


class SeoDataForm(ModelForm):
    class Meta:
        model = SeoData
        fields = ['title', 'url', 'keywords', 'description', 'seo_text']
        widgets = {
            'title': TextInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'Title',
            }),
            'url': URLInput(attrs={
                'required': 'required',
                'class': 'form-control',
                'placeholder': 'URL',
            }),
            'keywords': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Input text',
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Input text',
            }),
            'seo_text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Input text',
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
                  'is_2d', 'is_3d', 'is_imax']
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
                'placeholder': 'Input text',
            }),
            'trailer_url': URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Input text',
            }),
            'release_date': DateInput(attrs={
                'class': 'form-control',
                'placeholder': 'Input text',
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
                'placeholder': 'Input text',
            }),
            'conditions': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Input text',
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

from cinema_site.models import Movie, MovieGalleryImage, SeoData
from django.forms import CheckboxInput, DateInput, Form, ImageField, ModelForm, Textarea, TextInput, URLInput


class MovieGalleryImageForm(ModelForm):
    class Meta:
        model = MovieGalleryImage
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

# class MovieSeoMultiForm(MultiModelForm):
#     form_classes = {
#         'movie': MovieForm,
#         'seo': SeoDataForm,
#     }
#
#     field_order = ['first_name', 'language', 'last_name', 'gender', 'username', 'phone_number',
#                    'email', 'birthday', 'address', 'city', 'new_password', 'confirm_password', 'cc_number']
#
#     def clean(self):
#         cd = self.cleaned_data
#         if cd.get('new_password') != cd.get('confirm_password'):
#             self.add_error('confirm_password', 'passwords do not match !')
#             self.add_error('new_password', 'passwords do not match !')
#         return cd

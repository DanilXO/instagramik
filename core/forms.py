from django import forms
from django.core.exceptions import ValidationError

from core.models import Post, Comment, Profile


class PostForm(forms.ModelForm):
    max_size_img = 5
    # Можно задать  поле и таким образом, если форма. например, не для модели.
    # image = forms.ImageField(label=_('Change photo'), required=False, error_messages={'invalid': _
    # ("Image files only")}, widget=FileInput)

    class Meta:
        # Указываем модель
        model = Post
        # Указываем поля из модели
        fields = ['description', 'image']
        labels = {
            'description': 'Описание поста',
            'image': 'Выберите файл',
        }
        # Можем переопределить виджеты
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание поста'}),
            'image': forms.ClearableFileInput(attrs={'type': "file", 'class': "form-control-file"})
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > self.max_size_img*1024*1024:
                raise ValidationError("Файл должен быть не больше {0} мб".format(self.max_size_img))
            return image
        else:
            raise ValidationError("Не удалось прочитать файл")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Текст комментария'})
        }


from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):

    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'placeholder': 'Username',
                                                           'class': 'form-control'}))

    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder': 'Пароль', 'class': 'form-control'}),
    )

    error_messages = {
        'invalid_login': "Введен неправильный логин или пароль",
    }


class SignupForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Пароли не совпадают.",
    }

    password1 = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )

    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Подтвердите пароль'}),
        strip=False,
        help_text="Введите тот же пароль, что и выше",
    )

    class Meta:
        model = User
        fields = ('email', 'username')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Email'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email addresses must be unique.')
        return email


class UpdateProfileForm(forms.ModelForm):
    max_size_img = 3
    date_birth = forms.DateField(label="Дата рождения", input_formats=['%d-%m-%Y'],
                                 widget=forms.DateInput(format=('%d-%m-%Y'),
                                                        attrs={'class': 'form-control',
                                                              'placeholder': 'Дата рождения в формате dd-mm-yyyy'}))

    class Meta:
        model = Profile
        fields = ['date_birth', 'about', 'avatar']
        labels = {
                'about': "Обо мне",
                'avatar': "Аватар",
                }
        widgets = {
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Обо мне'}),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > self.max_size_img*1024*1024:
                raise ValidationError("Файл должен быть не больше {0} мб".format(self.max_size_img))
            return image
        else:
            raise ValidationError("Не удалось прочитать файл")


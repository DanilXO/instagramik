from django import forms
from django.core.exceptions import ValidationError

from core.models import Post


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

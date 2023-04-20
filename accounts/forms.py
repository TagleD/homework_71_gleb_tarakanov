from django import forms
from django.contrib.auth import get_user_model
from django.forms import TextInput, FileInput


class LoginForm(forms.Form):
    email = forms.EmailField(required=True, label='Электронный адрес')
    password = forms.CharField(required=True, label='Пароль', widget=forms.PasswordInput)


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', strip=False, required=True, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', strip=False, required=True,
                                       widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None

    class Meta:
        model = get_user_model()
        fields = (
            'username', 'password', 'password_confirm',
            'first_name', 'description',
            'phone', 'email', 'avatar',
            'gender'
        )
        widgets = {
            'username': TextInput(attrs={'placeholder': 'Логин'}),
            'first_name': TextInput(attrs={'placeholder': 'Имя'}),
            'description': TextInput(attrs={'placeholder': 'Информация о пользователе'}),
            'phone': TextInput(attrs={'placeholder': '+77077077777'}),
            'avatar': FileInput(attrs={'enctype': 'multipart/form-data'})
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'email', 'avatar', 'phone', 'description', 'gender')
        widgets = {
            'first_name': TextInput(attrs={'placeholder': 'Имя'}),
            'email': TextInput(attrs={'placeholder': 'Электронный адрес'}),
            'description': TextInput(attrs={'placeholder': 'Информация о пользователе'}),
            'phone': TextInput(attrs={'placeholder': '+77077077777'}),
            'avatar': FileInput(attrs={'enctype': 'multipart/form-data'})
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='Найти')

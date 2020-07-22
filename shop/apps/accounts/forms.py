from django import forms
from django.contrib.auth import get_user_model
from shop.apps.accounts.models import CustomUser

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Введенные пароли отличаются')
        return password2


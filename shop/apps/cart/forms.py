from django import forms


class CheckoutForm(forms.Form):
    city = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'autocomplete': 'off',
    }))
    street = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'autocomplete': 'off',
    }))
    house = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'autocomplete': 'off',
    }))
    flat = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'autocomplete': 'off',
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'placeholder': 'Имя',
        'autocomplete': 'off',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'placeholder': 'Фамилия',
        'autocomplete': 'off',
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        "class": 'form-control',
        'placeholder': '+7 *** *******',
        'autocomplete': 'off',
    }))
    email = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control",
        'placeholder': 'Email',
        'autocomplete': 'off',
    }))


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Введите номер промокода',
        'aria-label': 'Recipient\`s username',
        'aria-describedby': 'basic-addon2',
        'autocomplete': 'off',
    }))



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
    #payment_option = forms.BooleanField(widget=forms.RadioSelect())



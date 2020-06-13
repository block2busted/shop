from django.forms import ModelForm, widgets
from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        widgets = {
            'product': widgets.HiddenInput,
            'author': widgets.HiddenInput,
        }
        labels = {
            'plus': 'Преимущества',
            'minus': 'Недостатки'
        }
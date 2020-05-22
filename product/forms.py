from django.forms import ModelForm, Textarea
from django import forms
from .models import Review

RATING_CHOICES = ((0,'0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
)
class ReviewForm(ModelForm):
    #image = forms.ImageField()
    #if we include the above line then selecting an image is compulsory
    rating = forms.ChoiceField(choices = RATING_CHOICES)
    class Meta:
        model = Review
        fields = ['rating', 'content','image']
        widgets = {
            'content': Textarea(attrs={'cols': 40, 'rows': 15})
        }

class ReviewUpdateForm(ModelForm):
    #rating = forms.ChoiceField(choices=RATING_CHOICES)
    class Meta:
        model = Review
        fields = ['rating', 'content', 'image']
        widgets = {
            'content': Textarea(attrs={'cols': 40, 'rows': 15})
        }

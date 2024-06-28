from django import forms
from .models import *

class TouristplacesForm(forms.ModelForm):
    class Meta:
        model = Touristplaces
        fields = '__all__'

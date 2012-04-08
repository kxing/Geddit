from django.db import models
from django import forms
from data.models import Item

class ItemForm(forms.ModelForm):
    
    class Meta:
        model = Item
        fields = ('name', 'description', 'category', 'price', 'image')

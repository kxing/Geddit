from django.forms import ModelForm
from django.db import models
from data.models import Item

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'category', 'price')
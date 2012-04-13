from django.db import models
from django import forms
from data.models import Item, User, Reservation

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ('name', 'description', 'category', 'price', 'image')

class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('cell_phone', 'location')

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ('search_query', 'max_price')

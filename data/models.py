from django.db import models

USERNAME_MAX_LENGTH = 25
PERSON_NAME_MAX_LENGTH = 25

class User(models.Model):
    user_id = models.IntegerField()
    username = models.CharField(max_length=USERNAME_MAX_LENGTH)
    first_name = models.CharField(max_length=PERSON_NAME_MAX_LENGTH)
    last_name = models.CharField(max_length=PERSON_NAME_MAX_LENGTH)
    email = models.EmailField()

ITEM_NAME_MAX_LENGTH = 100
DESCRIPTION_NAME_MAX_LENGTH = 1000

class Item(models.Model):
    item_id = models.IntegerField()
    seller_user_id = models.IntegerField()
    name = models.CharField(max_length=ITEM_NAME_MAX_LENGTH)
    description = models.CharField(max_length=ITEM_NAME_MAX_LENGTH)
    active = models.BooleanField()
    category = models.IntegerField()

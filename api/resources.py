from tastypie.resources import ModelResource
from tastypie import fields
from geddit.data.models import User, Claim, Reservation, Category, Item
from tastypie.constants import ALL, ALL_WITH_RELATIONS

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email']
        filtering = {
            "username": ALL,
        }

class ItemResource(ModelResource):
    #category = fields.ForeignKey(CategoryResource, 'category')
    seller_user = fields.ForeignKey(UserResource, 'seller_user')
    
    class Meta:
        queryset = Item.objects.all()
        resource_name = 'item'
        excludes = ['resource_uri']

        filtering = {
            "name": ALL,
            "category": ALL_WITH_RELATIONS,
            "seller_user": ALL_WITH_RELATIONS
        }
        
class ClaimResource(ModelResource):
    buyer = fields.ForeignKey(UserResource, 'user')
    item = fields.ForeignKey(ItemResource, 'item')
    
    class Meta:
        queryset = Claim.objects.all()
        resource_name = 'claim'
        filtering = {
            "buyer": ALL_WITH_RELATIONS,
            "item": ALL_WITH_RELATIONS,
        }

class CategoryResource(ModelResource):
    items = fields.ToManyField(ItemResource,
        attribute=lambda bundle: Item.objects.filter(category=bundle.obj))
    
    class Meta:
        queryset = Category.objects.all()
        resource_name = 'category'
        excludes = ['resource_uri']
        filtering = {
            "name": ALL_WITH_RELATIONS,
        }

class ReservationResource(ModelResource):
    user = fields.ToOneField(UserResource, 'user')
    class Meta:
        queryset = Reservation.objects.all()
        resource_name = 'filter'
        filtering = {
            "user": ALL_WITH_RELATIONS,
        }

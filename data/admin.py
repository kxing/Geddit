from data.models import User, Category, Item, Filter, Claim, Location
from django.contrib import admin

class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields' : ['name']}),
        ('Geographic Information',
            {'fields': ['longitude', 'latitude']}
         ),
    ]
    list_display = ['name', 'longitude', 'latitude']
admin.site.register(Location, LocationAdmin)

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username']}),
        ('Personal Information',
            {'fields': ['first_name', 'last_name', 'email', 'cell_phone', 'location']}
        ),
    ]
    list_display = ['username', 'first_name', 'last_name', 'email', 'cell_phone', 'location']
admin.site.register(User, UserAdmin)

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']})
    ]
    list_display = ['name']
admin.site.register(Category, CategoryAdmin)

class ItemAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']}),
        ('Item Information',
            {'fields': ['description', 'category', 'claimed',
            'seller_user', 'upload_time', 'price']}
        ),
        ('Media',
            {'fields': ['image']}
        )
    ]
    list_display = ['name', 'category', 'claimed', 'seller_user', 'price']
admin.site.register(Item, ItemAdmin)

class FilterAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'search_query', 'timestamp']})
    ]
    list_display = ['user', 'search_query', 'timestamp']
admin.site.register(Filter, FilterAdmin)

class ClaimAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['buyer', 'item']})
    ]
    list_display = ['buyer', 'item']
admin.site.register(Claim, ClaimAdmin)


from data.models import User, Category, Item, Filter, Claim
from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['username']}),
        ('Personal Information',
            {'fields': ['first_name', 'last_name', 'email', 'cell_phone']}
        ),
    ]
    list_display = ['username', 'first_name', 'last_name', 'email', 'cell_phone']


admin.site.register(User, UserAdmin)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Filter)
admin.site.register(Claim)


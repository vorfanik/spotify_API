from django.contrib import admin
from .models import Users, Collection


class UsersAdmin(admin.ModelAdmin):
    list_display = ('user', 'f_name', 'l_name', 'city')

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'music')

admin.site.register(Users, UsersAdmin)
admin.site.register(Collection, CollectionAdmin)

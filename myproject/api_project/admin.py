from django.contrib import admin
from .models import Profile, Collection


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username',)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'artist')

admin.site.register(Profile, UsersAdmin)
admin.site.register(Collection, CollectionAdmin)

from django.contrib import admin
from .models import Profile, Collection, Recommendation


class UsersAdmin(admin.ModelAdmin):
    list_display = ('username',)

class CollectionAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'artist')

class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('genres',)

admin.site.register(Profile, UsersAdmin)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Recommendation, RecommendationAdmin)

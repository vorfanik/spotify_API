from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('album/<album_id>', views.album_info, name='album'),
    path('artist/<artist_id>', views.artist_info, name='artist'),
    path('search/', views.search, name='search'),
    path('collection/', views.collection, name='collection'),
    path('related_artists/<artist_id>', views.related_artists, name='related'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile_update/', views.profile_update, name='profile_update'),
]
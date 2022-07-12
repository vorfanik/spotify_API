from django.shortcuts import render, get_object_or_404, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.http import HttpResponse
from .spotify_requests import authorize
from .models import Users, Collection
import string
import random

api = authorize()

def index(request):
    random_album_name = ''.join(random.choices(string.ascii_letters, k=1))
    random_albums = api.search(random_album_name, types=('album',), limit=12)
    albums = random_albums[0].items
    context = {
        'albums': albums,
    }
    return render(request, 'index.html', context=context)

def album_info(request, album_id):
    album = api.album(album_id)
    return render(request, 'album.html', {'album': album})

def artist_info(request, artist_id):
    artist = api.artist(artist_id)
    artist_albums = api.artist_albums(artist_id, limit=50)
    context = {
        'artist': artist,
        'albums': artist_albums,
    }
    return render(request, 'artist.html', context=context)

def related_artists(request, artist_id):
    related = api.artist_related_artists(artist_id)
    return render(request, 'related.html', {'related': related})

def search(request):
    query = request.GET.get('query')
    search_results = api.search(query, types=('artist',), limit=12, offset=0)
    context = {
        'query': query,
        'results':search_results,
    }
    return render(request, 'search.html', context=context)
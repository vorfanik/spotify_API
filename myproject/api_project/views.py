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
from .models import Profile, Collection
from .forms import ProfileUpdateForm, UserUpdateForm
import string
import random
import re

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

@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{4,12}$"
            match_re = re.compile(reg)
            if re.search(match_re, password):
                # tikriname, ar neužimtas username
                if User.objects.filter(username=username).exists():
                    messages.error(request, _('User name %s already exists!') % username)
                    return redirect('register')
                else:
                    # tikriname, ar nėra tokio pat email
                    if User.objects.filter(email=email).exists():
                        messages.error(request, _('User with email Email %s is already registered!') % email)
                        return redirect('register')
                    else:
                        # jeigu viskas tvarkoje, sukuriame naują vartotoją
                        User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                        return redirect('login')
            else:
                messages.error(request, _('Please enter password should be One Capital Letter, One lowercase letter, One Number, Length Should be 4-12'))
                return redirect('register')
        else:
            messages.error(request, _('Passwords do not match!'))
            return redirect('register')
    return render(request, 'registration/register.html')

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def profile_update(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, _("Profile updated"))
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile_update.html', context)
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from .spotify_authorization import authorize
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
    collection = Collection.objects.filter(user=request.user.profile)
    exist = ""
    for albums in collection.values("album"):
        if albums['album'] == album_id:
            exist = albums['album']
    context = {
        'album': album,
        'exist': exist,
    }
    if request.method == 'POST':
        if request.POST.get("btn") == "add_form":
            if Collection.objects.filter(album = album_id).exists():
                return render(request, 'album.html', context=context)
            else:
                add = Collection.objects.create(artist ="Null", album=album_id, user=request.user.profile)
        elif request.POST.get("btn") == "del_form":
            Collection.objects.filter(album=album_id).delete()
            return redirect('/api_project/collection/')
    return render(request, 'album.html', context=context)


def artist_info(request, artist_id):
    artist = api.artist(artist_id)
    artist_albums = api.artist_albums(artist_id, limit=50)
    collection = Collection.objects.filter(user=request.user.profile)
    for artists in collection.values("artist"):
        exist = ""
        if artists['artist'] == artist_id:
            exist = artists['artist']
    context = {
        'artist': artist,
        'albums': artist_albums,
        'exist': exist,
    }
    if request.method == 'POST':
        if request.POST.get("btn") == "add_form":
            if Collection.objects.filter(artist = artist_id).exists():
                return render(request, 'artist.html', context=context)
            else:
                add = Collection.objects.create(artist =artist_id, album="Null", user=request.user.profile)
        elif request.POST.get("btn") == "del_form":
            Collection.objects.filter(artist=artist_id).delete()
            return redirect('/api_project/collection/')
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


@login_required
def collection(request):
    collection = Collection.objects.filter(user=request.user.profile)
    artists = []
    albums = []
    for artist in collection.values("artist"):
        if artist['artist'] != "Null":
            artists.append(api.artist(artist['artist']))
        else: continue
    for album in collection.values("album"):
        if album['album'] != "Null":
            albums.append(api.album(album['album']))
        else: continue
    context = {
        'artists': artists,
        'albums': albums,
    }
    return render(request, 'my_collection.html', context=context)


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
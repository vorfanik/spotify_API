from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(default="default.jpg", upload_to="profile_photo")

    def __str__(self):
        return f"{self.username} profile"

    class Meta:
        verbose_name = 'Users'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (250, 250)
            img.thumbnail(output_size)
            img.save(self.photo.path)

class Collection(models.Model):
    artist = models.CharField('artist_id', max_length=100, null=True)
    album = models.CharField('album_id', max_length=100, null=True)
    user = models.ForeignKey(Profile, verbose_name='User', on_delete=models.SET_NULL, null=True, blank=True, related_name='user')

    def __str__(self):
        return f"{self.user.username} - {self.artist} - {self.album}"

    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'

class Recommendation(models.Model):
    genres = models.CharField('genres', max_length=50)

    def __str__(self):
        return f"{self.genres}"
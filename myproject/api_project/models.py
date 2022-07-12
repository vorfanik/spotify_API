from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    f_name = models.CharField(verbose_name='Name', max_length=100)
    l_name = models.CharField(verbose_name='Last name', max_length=100)
    city = models.CharField(verbose_name='City', max_length=100)
    photo = models.ImageField(default="default.jpg", upload_to="profile_photo")

    def __str__(self):
        return f"{self.user.username}, {self.f_name}, {self.l_name}, {self.city}"

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.photo.path)
        if img.height > 300 or img.width > 300:
            output_size = (250, 250)
            img.thumbnail(output_size)
            img.save(self.photo.path)

class Collection(models.Model):
    music = models.CharField('Music_id', max_length=100)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.music}"

    class Meta:
        verbose_name = 'Collection'
        verbose_name_plural = 'Collections'
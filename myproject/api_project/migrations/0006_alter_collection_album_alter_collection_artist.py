# Generated by Django 4.0.6 on 2022-07-13 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_project', '0005_alter_collection_album_alter_collection_artist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='album',
            field=models.CharField(max_length=100, null=True, verbose_name='album_id'),
        ),
        migrations.AlterField(
            model_name='collection',
            name='artist',
            field=models.CharField(max_length=100, null=True, verbose_name='artist_id'),
        ),
    ]

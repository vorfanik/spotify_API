# Generated by Django 4.0.6 on 2022-07-14 07:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_project', '0010_recomendations'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Recomendations',
            new_name='Recommendation',
        ),
    ]

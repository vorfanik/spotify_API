# Generated by Django 4.0.6 on 2022-07-14 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_project', '0011_rename_recomendations_recommendation'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Recommendation',
        ),
    ]

# Generated by Django 4.0.6 on 2022-07-18 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api_project', '0013_recommendation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api_project.profile', verbose_name='User'),
        ),
    ]

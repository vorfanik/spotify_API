# Generated by Django 4.0.6 on 2022-07-14 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_project', '0012_delete_recommendation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genres', models.CharField(max_length=50, verbose_name='genres')),
            ],
        ),
    ]

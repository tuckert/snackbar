# Generated by Django 3.0.5 on 2020-05-11 22:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snackbar', '0002_snackbar_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snackbar',
            name='slug',
        ),
    ]

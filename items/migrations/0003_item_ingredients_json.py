# Generated by Django 3.0.6 on 2020-05-12 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_remove_category_snack_bar'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='ingredients_json',
            field=models.TextField(blank=True),
        ),
    ]

# Generated by Django 4.2.5 on 2023-10-06 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0011_alter_room_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]

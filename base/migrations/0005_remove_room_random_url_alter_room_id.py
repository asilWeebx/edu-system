# Generated by Django 4.2.5 on 2023-10-06 19:19

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_room_random_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='room',
            name='random_url',
        ),
        migrations.AlterField(
            model_name='room',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]

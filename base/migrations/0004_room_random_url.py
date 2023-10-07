# Generated by Django 4.2.5 on 2023-10-06 18:59

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_room_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='random_url',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
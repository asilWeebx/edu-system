# Generated by Django 4.2.5 on 2023-10-06 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(default=1, upload_to='images_gr/'),
            preserve_default=False,
        ),
    ]

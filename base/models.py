from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from app.models import Grade
import uuid
import random
from django.template.defaultfilters import slugify
User = get_user_model()

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

upper ="QWERTYUIOPASDFGHJKLZXCVBNM"
lower ="qwertyuiopasdfghjklzxcvbnm"
numbers = "0123456789"
string = upper + lower + numbers
lengt = 16
url = "".join(random.sample(string,lengt))

class Room(models.Model):
    slug = models.SlugField(unique=True,blank=True)
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images_gr/",blank=True)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(url)
        super(Room,self).save(*args,**kwargs)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

from django.db import models
from froala_editor.fields import FroalaField
from django.contrib.auth.models import User


# Create your models here.


class post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    desc = FroalaField(theme='dark')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Contact(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    address = models.CharField(max_length=300)
    message = FroalaField()

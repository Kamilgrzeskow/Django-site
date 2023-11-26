from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Kontakt(models.Model):
    imie = models.CharField(max_length=50)
    nazwisko = models.CharField(max_length=150)
    telefon = models.IntegerField()
    email = models.EmailField(max_length=100, default="")


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Title = {self.title}, content = {self.content}, date of the post = {self.date_posted}, author = {self.author}"


    def get_absolute_url(self):
        return reverse('post-detail', kwargs= {'pk':self.pk})
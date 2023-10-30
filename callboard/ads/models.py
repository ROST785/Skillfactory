from django.db import models
from django.contrib.auth.models import User

CATEGORIES = [("Танки", "Хилы", "ДД", "Торговцы", "Гилдмастеры", "Квестгиверы", "Кузнецы", "Кожевники", "Зельевары", "Мастера заклинаний")]


class Announcement(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', through='AnnouncementCategory')
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(null=False)


class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField(max_length=255, null=False)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    subscribers = models.ManyToManyField(User, related_name='categories')


class AnnouncementCategory(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from django.db import models


class User(AbstractUser):
    pass


class Categorie(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"


class Item(models.Model):
    image = models.URLField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=64)
    description = models.TextField(default="")
    category = models.ForeignKey(
        Categorie, on_delete=models.PROTECT , blank=True, null=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}"

class Price(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"{self.price} at {self.item} created by {self.user}"


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.comment} at {self.item}"

class Watchlist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item} listed by {self.user}"

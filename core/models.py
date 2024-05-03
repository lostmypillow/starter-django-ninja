from django.db import models


# Create your models here.

class Deck(models.Model):
    objects = None
    creation_date = models.DateTimeField("creation date")


class Card(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    suit = models.CharField(default="hearts", max_length=200)
    value = models.CharField(default="5", max_length=200)

    def __str__(self):
        return self.value

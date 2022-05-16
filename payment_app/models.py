from django.db import models


# Create your models here.
class ItemModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.IntegerField()

    def __str__(self):
        return self.name

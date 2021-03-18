from django.db import models

# Create your models here.
class Store(models.Model):
    store_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    address = models.TextField()
    nearby = models.BooleanField() # null=True, default=True
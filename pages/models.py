from django.db import models


class Car(models.Model):
    plate = models.CharField(max_length=64, unique=True, blank=False)


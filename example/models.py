from django.db import models


class About(models.Model):
    name = models.CharField(max_length=55)
    state = models.CharField(max_length=55)
    lga = models.CharField(max_length=55)

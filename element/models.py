from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.
# Extra objects that may be required but are not essential
class Substrate(models.Model):

    name = models.CharField(max_length=200, unique=True)

    type = models.CharField(max_length=200)

    source = models.CharField(max_length=200)

    cost = models.FloatField(validators=[MinValueValidator(0)])

    observations = models.TextField()

    def __str__(self):
        return self.name


class Microorganism(models.Model):

    name = models.CharField(max_length=200, unique=True)

    type = models.CharField(max_length=200)

    source = models.CharField(max_length=200)

    cost = models.FloatField(validators=[MinValueValidator(0)])

    optimal_conditions = models.TextField()

    observations = models.TextField()

    def __str__(self):
        return self.name


class Product(models.Model):

    name = models.CharField(max_length=200, unique=True)

    type = models.CharField(max_length=200)

    market_value = models.FloatField(validators=[MinValueValidator(0)])

    detection_method = models.CharField(max_length=200)

    observations = models.TextField()

    def __str__(self):
        return self.name

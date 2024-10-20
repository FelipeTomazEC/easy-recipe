from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator
from djmoney.models.fields import MoneyField

from enum import Enum

class Unit(Enum):
    GRAM = 'g'
    KILOGRAM = 'Kg'
    LITER = 'L'
    CENTILITER = 'cl'

class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    ean = models.CharField(primary_key=True, max_length=13, validators=[MinLengthValidator(13), MaxLengthValidator(13)])
    standard_amount = models.BigIntegerField(validators=[MinValueValidator(0)])
    standard_unit = models.CharField(max_length=20, choices=[(unit.name, unit.value) for unit in Unit])
    cost_per_unit = MoneyField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name




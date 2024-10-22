from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from djmoney.money import Money

from ingredients.models import Ingredient


class Recipe(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.RESTRICT)
    amount = models.FloatField(validators=[MinValueValidator(0)])
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def get_cost(self):
        return self.amount * self.ingredient.cost_per_unit
from functools import reduce
from django.core.validators import MinValueValidator, MinLengthValidator
from django.db import models
from djmoney.money import Money

from ingredients.models import Ingredient

from .helpers import EurConverter

class Recipe(models.Model):
    name = models.CharField(max_length=100, validators=[MinLengthValidator(3)])
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    def get_total_cost_in_eur(self):
        recipe_ingredients = RecipeIngredient.objects.filter(recipe=self)
        individual_ingredients_cost = map(lambda ingredient: ingredient.get_cost_in_eur(), recipe_ingredients)
        total_cost = reduce(lambda cost_one, cost_two: cost_one + cost_two, individual_ingredients_cost, Money(0, 'EUR'))
        return total_cost


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.RESTRICT)
    amount = models.FloatField(validators=[MinValueValidator(0)])
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def get_cost_in_eur(self):
        cost_in_registered_currency = self.amount * (self.ingredient.cost_per_unit / self.ingredient.standard_amount)
        eur_converter = EurConverter()
        return eur_converter.convert(cost_in_registered_currency)
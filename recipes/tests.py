from math import ceil
import random

from django.test import TestCase
from unittest.mock import patch
from djmoney.money import Money

from ingredients.models import Ingredient, Unit
from .models import RecipeIngredient, Recipe
from .helpers import EurConverter

def create_test_ingredient(cost, unit = Unit.KILOGRAM, standard_amount = 1,currency = 'EUR'):
    standard_unit = unit.value
    cost_per_unit = Money(cost, currency)
    
    return Ingredient.objects.create(
        name=f"Ingredient_{random.random()}", 
        cost_per_unit=cost_per_unit, 
        standard_amount=standard_amount,
        standard_unit=standard_unit,
        ean=f"123456789{random.randint(1000, 9999)}"
    )

@patch('recipes.helpers.EurConverter.convert')
class RecipeIngredientModelTests(TestCase):
    def test_get_cost_in_eur(self, mock_eur_converter):
        mock_eur_converter.side_effect = lambda money: Money(float(money.amount) * 0.2, 'EUR')
        cost_per_unit = Money(10, 'BRL')
        standard_unit = Unit.GRAM.value
        standard_amount = 500
        ingredient = Ingredient(standard_unit=standard_unit, cost_per_unit=cost_per_unit, standard_amount = standard_amount)

        recipe_ingredient_amount = 250
        recipe_ingredient = RecipeIngredient(ingredient=ingredient, amount=recipe_ingredient_amount)
        
        total_cost_in_eur = recipe_ingredient.get_cost_in_eur()

        self.assertEqual(total_cost_in_eur, Money(1, 'EUR'))

class RecipeModelTests(TestCase):

    @patch('recipes.helpers.EurConverter.convert')
    def test_get_recipe_total_cost(self, mock_eur_converter):
        mock_eur_converter.side_effect = lambda arg: arg

        recipe = Recipe.objects.create(name="My Recipe")

        ingredient1 = create_test_ingredient(cost=2)
        ingredient2 = create_test_ingredient(cost=3)

        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient1, amount=0.5)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient2, amount=2)

        recipe_total_cost = recipe.get_total_cost_in_eur()

        self.assertEqual(recipe_total_cost, Money(7, 'EUR'))
    
    @patch('recipes.helpers.EurConverter.convert')
    def test_get_recipe_cost_single_ingredient(self, mock_eur_converter):
        mock_eur_converter.side_effect = lambda arg: arg

        recipe = Recipe.objects.create(name="Single ingredient recipe")

        ingredient = create_test_ingredient(cost=5)

        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, amount=2)

        recipe_total_cost = recipe.get_total_cost_in_eur()

        self.assertEqual(recipe_total_cost, Money(10, 'EUR'))

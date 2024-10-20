from django.test import TestCase

from djmoney.money import Money

from ingredients.models import Ingredient, Unit
from .models import RecipeIngredient


class RecipeIngredientModelTests(TestCase):
    def test_get_cost(self):
        cost_per_unit = Money(5, 'EUR')
        standard_unit = Unit.KILOGRAM.value
        ingredient = Ingredient(standard_unit=standard_unit, cost_per_unit=cost_per_unit)

        recipe_ingredient_amount = 0.5
        recipe_ingredient = RecipeIngredient(ingredient=ingredient, amount=recipe_ingredient_amount)
        
        total_cost = recipe_ingredient.get_cost()

        self.assertEqual(total_cost, Money(2.5, 'EUR'))
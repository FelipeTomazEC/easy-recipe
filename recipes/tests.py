import random

from django.test import TestCase

from djmoney.money import Money

from ingredients.models import Ingredient, Unit
from .models import RecipeIngredient, Recipe

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


class RecipeIngredientModelTests(TestCase):
    def test_get_cost(self):
        cost_per_unit = Money(1, 'EUR')
        standard_unit = Unit.GRAM.value
        standard_amount = 500
        ingredient = Ingredient(standard_unit=standard_unit, cost_per_unit=cost_per_unit, standard_amount = standard_amount)

        recipe_ingredient_amount = 100
        recipe_ingredient = RecipeIngredient(ingredient=ingredient, amount=recipe_ingredient_amount)
        
        total_cost = recipe_ingredient.get_cost()

        self.assertEqual(total_cost, Money(0.2, 'EUR'))

class RecipeModelTests(TestCase):
    def test_get_recipe_total_cost(self):
        recipe = Recipe.objects.create(name="My Recipe")

        ingredient1 = create_test_ingredient(cost=2)
        ingredient2 = create_test_ingredient(cost=3)

        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient1, amount=0.5)
        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient2, amount=2)

        recipe_total_cost = recipe.get_total_cost()

        self.assertEqual(recipe_total_cost, Money(7, 'EUR'))
    
    def test_get_recipe_cost_single_ingredient(self):
        recipe = Recipe.objects.create(name="Single ingredient recipe")

        ingredient = create_test_ingredient(cost=5)

        RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, amount=2)

        recipe_total_cost = recipe.get_total_cost()

        self.assertEqual(recipe_total_cost, Money(10, 'EUR'))

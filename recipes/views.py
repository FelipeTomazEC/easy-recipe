from django.db import transaction
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic

from ingredients.models import Ingredient

from .models import Recipe, RecipeIngredient

class SeeAllRecipesView(generic.ListView):
    context_object_name = 'recipe_list'
    template_name = 'recipes/index.html'

    def get_queryset(self):
        return Recipe.objects.all()

class RecipeDetailsView(generic.DetailView):
    template_name = 'recipes/recipe_details.html'
    model = Recipe

class AddRecipeView(generic.TemplateView):
    template_name = 'recipes/add_recipe.html'

    def post(self, request, *args, **kwargs):
        recipe_name = request.POST.get('name', '')
        recipe_ingredients = self.extract_recipe_ingredients()
        try:
            self.store_recipe(recipe_name, recipe_ingredients)
            return HttpResponseRedirect(reverse('recipes:index'))
        except ValidationError as e:
            errors = e.message_dict
            return self.render_to_response(self.get_context_data(errors = errors, name=recipe_name, ingredients=recipe_ingredients))
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredient_list"] = list(Ingredient.objects.all().values('ean', 'name', 'standard_unit'))
        return context
    
    def extract_recipe_ingredients(self):
        request_data = self.request.POST
        ingredients = []
        recipe_ingrediet_keys = filter(lambda key: key.startswith('ingredients[') and key.endswith('[ean]'), request_data.keys())

        for recipe_ingredient in recipe_ingrediet_keys:
            key = recipe_ingredient[0:14]
            ingredient = {
                'ean': request_data.get(f'{key}[ean]'),
                'amount': request_data.get(f'{key}[amount]')
            }
            ingredients.append(ingredient)
        
        return ingredients
    
    
    @transaction.atomic
    def store_recipe(self, name, recipe_ingredients):
        recipe = Recipe.objects.create(name = name)
        recipe.full_clean()
        self.store_ingredients(recipe=recipe, recipe_ingredients=recipe_ingredients)

    def store_ingredients(self, recipe, recipe_ingredients):
        print('Running base store ingredients')
        if (not recipe_ingredients):
            raise ValidationError({'ingredients': 'A recipe must have at least 1 ingredient.'})
        
        for recipe_ingredient_data in recipe_ingredients:
            ingredient = get_object_or_404(Ingredient, pk=recipe_ingredient_data['ean'])
            amount = recipe_ingredient_data['amount']

            if (not amount or float(amount) <= 0):
                raise ValidationError({'ingredients': 'All ingredients must have a non-zero amount'})

            RecipeIngredient.objects.create(ingredient=ingredient, amount=amount, recipe=recipe)

class EditRecipeView(AddRecipeView):
    template_name = 'recipes/edit_recipe.html'

    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            recipe = get_object_or_404(Recipe, pk=self.kwargs.get('pk'))
            context["name"] = recipe.name
            context["recipe"] = recipe
            context["ingredients"] = self.get_recipe_ingredients_for_context(recipe)
            return context

    def get_recipe_ingredients_for_context(self, recipe):
        context_recipe_ingredients = []
        
        for recipe_ingredient in recipe.recipeingredient_set.all():
            context_recipe_ingredients.append({
                "ean": recipe_ingredient.ingredient.ean,
                "amount": recipe_ingredient.amount
            })
        
        return context_recipe_ingredients
    
    @transaction.atomic
    def store_recipe(self, name, recipe_ingredients):
        recipe_id = self.kwargs.get('pk')
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.name = name
        recipe.full_clean()
        recipe.save()

        self.store_ingredients(recipe=recipe, recipe_ingredients=recipe_ingredients)

    def store_ingredients(self, recipe, recipe_ingredients):
        if (not recipe_ingredients):
            raise ValidationError({'ingredients': 'A recipe must have at least 1 ingredient.'})

        current_recipe_ingredients_eans = list(map(lambda ingredient: ingredient.ean, recipe.ingredients.all()))
        recipe_ingredients_eans_from_request = list(map(lambda recipe_ingredient: recipe_ingredient['ean'], recipe_ingredients))
        removed_ingredients = list(filter(lambda ean: ean not in recipe_ingredients_eans_from_request, current_recipe_ingredients_eans))
        added_ingredients = list(filter(lambda ingredient: ingredient['ean'] not in current_recipe_ingredients_eans, recipe_ingredients))
        modified_ingredients = list(filter(lambda ingredient: ingredient['ean'] in current_recipe_ingredients_eans, recipe_ingredients))

        
        RecipeIngredient.objects.filter(recipe_id=recipe.id, ingredient_id__in=removed_ingredients).delete()
        
        for added_ingredient in added_ingredients:
            amount = added_ingredient['amount']
            if (not amount or float(amount) <= 0):
                raise ValidationError({'ingredients': 'All ingredients must have a non-zero amount'})

            ingredient = get_object_or_404(Ingredient, pk=added_ingredient['ean'])
            RecipeIngredient.objects.create(ingredient=ingredient, amount=amount, recipe=recipe)
        
        for modified_ingredient in modified_ingredients:
            amount = modified_ingredient['amount']
            if (not amount or float(amount) <= 0):
                raise ValidationError({'ingredients': 'All ingredients must have a non-zero amount'})
            recipe_ingredient = get_object_or_404(RecipeIngredient, recipe_id=recipe.id, ingredient_id=modified_ingredient['ean'])
            recipe_ingredient.amount = amount
            recipe_ingredient.save()
        






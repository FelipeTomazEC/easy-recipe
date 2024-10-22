from django.db import transaction
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

from ingredients.models import Ingredient

from .models import Recipe, RecipeIngredient

class SeeAllRecipesView(generic.ListView):
    context_object_name = 'recipe_list'
    template_name = 'recipes/index.html'

    def get_queryset(self):
        return Recipe.objects.all()

class AddRecipeView(generic.TemplateView):
    template_name = 'recipes/add_recipe.html'

    def post(self, request, *args, **kwargs):
        recipe_name = request.POST.get('name', '')
        recipe_ingredients = self.extract_recipe_ingredients(request)
        try:
            self.store_recipe(recipe_name, recipe_ingredients)
            return HttpResponseRedirect(reverse('recipes:index'))
        except ValidationError as e:
            errors = e.message_dict
            print(recipe_name)
            return self.render_to_response(self.get_context_data(errors = errors, name=recipe_name, ingredients=recipe_ingredients))
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ingredient_list"] = list(Ingredient.objects.all().values('ean', 'name', 'standard_unit'))
        return context
    
    def extract_recipe_ingredients(self, request):
        request_data = request.POST
        ingredients = []
        index = 0

        while True:
            ean_key = f'ingredients[{index}][ean]'
            amount_key = f'ingredients[{index}][amount]'

            if ean_key in request_data and amount_key in request_data:
                ingredient = {
                    'ean': request_data.get(ean_key),
                    'amount': request_data.get(amount_key),
                }
                ingredients.append(ingredient)
            else:
                break  #There are no more ingredients

            index += 1
        
        return ingredients
    
    
    @transaction.atomic
    def store_recipe(self, name, recipe_ingredients):
        recipe = Recipe.objects.create(name = name)
        recipe.full_clean()
        self.store_ingredients(recipe=recipe, recipe_ingredients=recipe_ingredients)

        
    
    def store_ingredients(self, recipe, recipe_ingredients):
        if (not recipe_ingredients):
            raise ValidationError({'ingredients': 'A recipe must have at least 1 ingredient.'})
        
        for recipe_ingredient_data in recipe_ingredients:
            ingredient = get_object_or_404(Ingredient, pk=recipe_ingredient_data['ean'])
            amount = recipe_ingredient_data['amount']

            if (not amount or float(amount) <= 0):
                raise ValidationError({'ingredients': 'All ingredients must have a non-zero amount'})

            ingredient = RecipeIngredient.objects.create(ingredient=ingredient, amount=amount, recipe=recipe)
        



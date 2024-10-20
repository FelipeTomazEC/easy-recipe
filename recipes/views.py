from django.views import generic

from .models import Recipe

class SeeAllRecipesView(generic.ListView):
    context_object_name = 'recipe_list'
    template_name = 'recipes/index.html'

    def get_queryset(self):
        return Recipe.objects.all()

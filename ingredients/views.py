from django.urls import reverse_lazy
from django.views import generic
from django.db.models import Q as FilterParam

from .forms import AddIngredientForm
from .models import Ingredient

class IndexView(generic.ListView):
    template_name = "ingredients/index.html"
    context_object_name = "ingredient_list"
    
    def get_queryset(self):
        search = self.request.GET.get('search_param', '')

        if search:
            return Ingredient.objects.filter(FilterParam(name__icontains=search) | FilterParam(ean__icontains=search))
        
        return Ingredient.objects.all()
    
class IngredientDetailsView(generic.DetailView):
    template_name = "ingredients/ingredient_details.html"
    model = Ingredient

class AddIngredientView(generic.CreateView):
    model = Ingredient
    form_class = AddIngredientForm
    template_name = "ingredients/add_ingredient.html"
    success_url = reverse_lazy('ingredients:index')

class EditIngredientView(generic.UpdateView):
    model = Ingredient
    form_class = AddIngredientForm
    template_name = "ingredients/edit_ingredient.html"
    success_url = reverse_lazy('ingredients:index')

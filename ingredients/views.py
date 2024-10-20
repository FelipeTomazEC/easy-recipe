from django.views import generic
from django.db.models import Q as FilterParam

from .models import Ingredient

class IndexView(generic.ListView):
    template_name = "ingredients/index.html"
    context_object_name = "ingredient_list"
    
    def get_queryset(self):
        search = self.request.GET.get('search_param', '')

        if search:
            return Ingredient.objects.filter(FilterParam(name__icontains=search) | FilterParam(ean__icontains=search))
        
        return Ingredient.objects.all()
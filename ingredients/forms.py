from django import forms
from djmoney.money import Money

from .models import Ingredient

class AddIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AddIngredientForm, self).__init__(*args, **kwargs)
        self.fields['cost_per_unit'].initial = Money(1.00, 'EUR')
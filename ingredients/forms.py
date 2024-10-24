from django import forms
from djmoney.forms.fields import MoneyField
from currency_converter.currency_converter import CurrencyConverter
from babel.numbers import get_currency_name

from .models import Ingredient

class AddIngredientForm(forms.ModelForm):
    suported_currencies = CurrencyConverter().currencies
    cost_per_unit = MoneyField(
        currency_choices=[(currency, get_currency_name(currency, locale="en_US")) for currency in suported_currencies],
        max_digits=10,
        decimal_places=2,
        default_currency='EUR',
        default_amount=1
    )

    class Meta:
        model = Ingredient
        fields = "__all__"
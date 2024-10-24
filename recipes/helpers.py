from currency_converter import CurrencyConverter
from djmoney.money import Money

class EurConverter():
    def convert(self, money):
        if money.currency.code == 'EUR':
            return money
        
        converter = CurrencyConverter()
        converted_amount = converter.convert(float(money.amount), money.currency.code, 'EUR')
        return Money(converted_amount, 'EUR')


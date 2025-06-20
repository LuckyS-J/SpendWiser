from django.forms import ModelForm, DateInput
from .models import Transaction
from datetime import datetime

class TransactionForm(ModelForm):
  class Meta:
    model = Transaction
    fields = ['title', 'amount', 'date', 'category']
    widgets = {
        'date': DateInput(attrs={'type': 'date'})
    }
from django.forms import ModelForm, DateInput, ValidationError
from .models import Transaction
import datetime
from .utils import assign_category


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ['title', 'amount', 'date', 'category']
        widgets = {
            'date': DateInput(attrs={'type': 'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].required = False

    def clean_date(self):
        date = self.cleaned_data['date']
        if date > datetime.date.today() or date.year < 2000:
            raise ValidationError("Invalid date")
        return date

    def clean_category(self):
        category = self.cleaned_data.get('category')
        if not category:
            title = self.cleaned_data.get('title', '')
            category = assign_category(title)
        return category

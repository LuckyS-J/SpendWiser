from django.db import models
from core.models import CustomUser
import datetime

# Create your models here.


class Transaction(models.Model):

    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('transport', 'Transport'),
        ('bills', 'Bills'),
        ('education', 'Education'),
        ('clothes', 'Clothes'),
        ('electronics', 'Electronics'),
        ('entertainment', 'Entertainment'),
        ('health', 'Health'),
        ('other', 'Other'),
    ]

    TYPE_CHOICES = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='transactions')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(default=datetime.date.today)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def save(self, *args, **kwargs):
        if self.amount >= 0:
            self.type = 'income'
        else:
            self.type = 'expense'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}, {self.amount}"

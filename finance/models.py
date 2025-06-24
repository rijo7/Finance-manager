from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
    ]

    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} - {self.name}"

class Transaction(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.category} - {self.subcategory} - {self.amount}"






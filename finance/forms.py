from django import forms
from .models import Transaction, Category, Subcategory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['category', 'subcategory', 'amount', 'date', 'description']

    def __init__(self, *args, **kwargs):
        super(TransactionForm, self).__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

        # Initially, subcategory field will be empty until a category is selected
        self.fields['subcategory'].queryset = Subcategory.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the user; ignore and leave queryset empty
        elif self.instance.pk:
            self.fields['subcategory'].queryset = self.instance.category.subcategories.order_by('name')





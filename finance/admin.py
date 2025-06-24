from django.contrib import admin
from .models import Category, Subcategory, Transaction

class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    inlines = [SubcategoryInline]

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('category', 'subcategory', 'amount', 'date', 'description', 'user')
    list_filter = ('category', 'subcategory', 'date')
    search_fields = ('description', 'amount', 'user__username')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Subcategory)
admin.site.register(Transaction, TransactionAdmin)

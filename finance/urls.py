from django.contrib import admin
from django.urls import path
from . import views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('home/', views.home, name='home'),  # Ensure this path exists
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add/', views.add_transaction, name='add_transaction'),
    path('edit/<int:id>/', views.edit_transaction, name='edit_transaction'),
    path('detail/<int:id>/', views.transaction_detail, name='transaction_detail'),
    path('list/', views.transaction_list, name='transaction_list'),
    path('delete/<int:id>/', views.delete_transaction, name='delete_transaction'),
    path('ajax/load-subcategories/', views.ajax_load_subcategories, name='ajax_load_subcategories'),
    path('export/transactions/pdf/', views.export_transactions_pdf, name='export_transactions_pdf'),

    # Redirect the root URL to the login page
    path('', RedirectView.as_view(url='/login/', permanent=True)),
]
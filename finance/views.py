import json
from django.http import JsonResponse
from django.http import HttpResponse
import pdfkit
from django.template.loader import render_to_string
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import Transaction, Category, Subcategory
from .forms import TransactionForm
from django.db.models import Sum
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'finance/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'finance/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Invalid username or password")
            return render(request, 'finance/login.html', {'error': 'Invalid username or password'})
    return render(request, 'finance/login.html')


def logout_user(request):
    auth_logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    # Calculate total income and expenses
    income = Transaction.objects.filter(user=request.user, category__name='income').aggregate(Sum('amount'))['amount__sum'] or 0
    expense = Transaction.objects.filter(user=request.user, category__name='expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = income - expense

    # Prepare data for the charts
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
              'November', 'December']

    # Initialize empty lists to hold monthly income and expense data
    income_data = [0] * 12
    expense_data = [0] * 12

    # Aggregating data by month
    monthly_income_data = Transaction.objects.filter(user=request.user, category__name='income').values('date__month').annotate(
        total=Sum('amount'))
    monthly_expense_data = Transaction.objects.filter(user=request.user, category__name='expense').values('date__month').annotate(
        total=Sum('amount'))

    # Populate income data for each month
    for entry in monthly_income_data:
        month = entry['date__month']
        if 1 <= month <= 12:
            income_data[month - 1] = float(entry['total'])

    # Prepare chart data for monthly income
    monthly_income_chart_data = json.dumps({
        'labels': months,
        'income_data': income_data,
    })

    # Populate expense data for each month
    for entry in monthly_expense_data:
        month = entry['date__month']
        if 1 <= month <= 12:
            expense_data[month - 1] = float(entry['total'])

    # Prepare chart data for income vs expense chart
    chart_data = {
        'labels': months,
        'income_data': income_data,
        'expense_data': expense_data,
    }

    # Compile the context dictionary to pass all required data to the template
    context = {
        'income': income,
        'expense': expense,
        'balance': balance,
        'chart_data': chart_data,
        'monthly_income_chart_data': monthly_income_chart_data,
    }

    return render(request, 'finance/dashboard.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()

    return render(request, 'finance/add_transaction.html', {'form': form})

def ajax_load_subcategories(request):
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
    return JsonResponse({'subcategories': list(subcategories.values('id', 'name'))})


@login_required
def edit_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'finance/edit_transaction.html', {'form': form})

@login_required
def transaction_detail(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    return render(request, 'finance/transaction_detail.html', {'transaction': transaction})

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    return render(request, 'finance/transaction_list.html', {'transactions': transactions})

@login_required
def delete_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'finance/delete_transaction.html', {'transaction': transaction})

def export_transactions_pdf(request):
    transactions = Transaction.objects.filter(user=request.user)
    html_string = render_to_string('finance/transactions_pdf.html', {'transactions': transactions})

    # Convert HTML string to PDF
    pdf_file = pdfkit.from_string(html_string, False)  # False means it will return a PDF file as bytes

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'

    return response

@csrf_exempt
def seed_categories(request):
    if request.method != "GET":
        return HttpResponse("Method Not Allowed", status=405)

    # Optional: add a secret check
    secret = request.GET.get('secret')
    if secret != 'YOUR_SECRET_KEY':
        return HttpResponse("Forbidden", status=403)

    # Clear existing data
    Subcategory.objects.all().delete()
    Category.objects.all().delete()

    # Create categories
    income = Category.objects.create(name='income')
    expense = Category.objects.create(name='expense')

    # Income subcategories
    income_subs = [
        'Other Income',
        'Gifts',
        'Investment Income',
        'Business Income',
        'Salary',
    ]
    for name in income_subs:
        Subcategory.objects.create(category=income, name=name)

    # Expense subcategories
    expense_subs = [
        'Other Expenses',
        'Medical',
        'Transportation',
        'Rent/Mortgage',
        'Entertainment',
        'Utilities',
        'Food',
    ]
    for name in expense_subs:
        Subcategory.objects.create(category=expense, name=name)

    return HttpResponse("Seeding complete ✅")
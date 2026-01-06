from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Expense

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def dashboard(request):
    category_filter = request.GET.get('category')

    expenses = Expense.objects.filter(user=request.user)

    if category_filter:
        expenses = expenses.filter(category=category_filter)

    total = sum(exp.amount for exp in expenses)

    return render(
        request,
        'dashboard.html',
        {
            'expenses': expenses,
            'total': total,
            'selected_food': category_filter == 'Food',
            'selected_travel': category_filter == 'Travel',
            'selected_shopping': category_filter == 'Shopping',
            'selected_rent': category_filter == 'Rent',
            'selected_others': category_filter == 'Others',
        }
    )


@login_required(login_url='login')
def add_expense(request):
    if request.method == "POST":
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        # Validation
        if not category:
            messages.error(request, "Category cannot be empty")
            return redirect('add_expense')

        if float(amount) <= 0:
            messages.error(request, "Amount must be greater than zero")
            return redirect('add_expense')

        Expense.objects.create(
            user=request.user,
            category=category,
            amount=amount,
            description=description
        )

        messages.success(request, "Expense added successfully")
        return redirect('dashboard')

    return render(request, 'add_expense.html')

@login_required(login_url='login')
def edit_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)

    if request.method == "POST":
        category = request.POST.get('category')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        # Validation
        if not category:
            messages.error(request, "Category cannot be empty")
            return redirect('edit_expense', id=id)

        if float(amount) <= 0:
            messages.error(request, "Amount must be greater than zero")
            return redirect('edit_expense', id=id)

        expense.category = category
        expense.amount = amount
        expense.description = description
        expense.save()

        messages.success(request, "Expense updated successfully")
        return redirect('dashboard')

    return render(request, 'edit_expense.html', {'expense': expense})

@login_required(login_url='login')
def delete_expense(request, id):
    expense = get_object_or_404(Expense, id=id, user=request.user)
    expense.delete()
    messages.success(request, "Expense deleted successfully")
    return redirect('dashboard')


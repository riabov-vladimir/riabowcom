from django.shortcuts import render
from budgetreport.models import *
from .forms import AdditionalExpensesForm
from django.http import HttpResponseRedirect



def budget_summary(request):

    employees = Employee.objects.all().order_by('position')
    positions = EmployeePosition.objects.all().order_by('position')
    additional_expenses = AdditionalExpenses.objects.all().order_by('-expense_value')

    if request.method == 'POST':

        form = AdditionalExpensesForm(request.POST)

        if form.is_valid():
            additional_expenses_item = AdditionalExpenses(expense_purpose=form.cleaned_data['expense_purpose'],
                                                          expense_value=form.cleaned_data['expense_value'])
            additional_expenses_item.save()
            return HttpResponseRedirect('/budgetreport/summary/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = AdditionalExpensesForm()

    context = {
        'employees': employees,
        'positions': positions,
        'additional_expenses': additional_expenses,
        'form': form
    }

    return render(request,
                  'budgetreport/budget_summary.html',
                  context
                  )
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import ListView
from budgetreport.models import *
from .forms import AdditionalExpensesForm, EmployeeHoursForm
from django.http import HttpResponseRedirect
from django.db.models import Sum, Model, PositiveIntegerField
from django.views.decorators.http import require_safe
from django.http import HttpResponse


# 1. Главная страница отчёта - общая информация с вкладки экселя "Счёт заказчику"
@require_safe
def budget_summary(request):
    user_group = list(request.user.groups.values_list('name', flat=True))
    if 'rd' not in user_group:
        return HttpResponseRedirect('/')

    # calculate full-price working hours cost
    employee_hours = EmployeeHours.objects.filter(is_discount_hours=False).all()
    employee_hours_cost = 0
    for i in employee_hours:
        employee_hours_cost += int(i.hours_cost())

    # calculate discounted working hours cost
    employee_discount_hours = EmployeeHours.objects.filter(is_discount_hours=True).all()
    employee_discount_hours_cost = 0
    for i in employee_discount_hours:
        employee_discount_hours_cost += int(i.discount_hours_cost())

    # calculate additional expenses total cost
    additional_expenses = AdditionalExpenses.objects.all() \
        .aggregate(Sum('expense_value')) \
        .get('expense_value__sum')
    if not additional_expenses:   # converts None to int for calculations
        additional_expenses = 0

    overall_cost = employee_discount_hours_cost + employee_hours_cost + additional_expenses

    context = {
        'overall_cost': overall_cost,
        'employee_hours_cost': employee_hours_cost,
        'employee_discount_hours_cost': employee_discount_hours_cost
    }

    return render(request,
                  'budgetreport/budget_summary.html',
                  context
                  )


# 2. Вкладка "Списанные часы", в экселе вкладка называлась по имени месяца отчёта
#   GET, POST
def employee_hours_view(request):
    employee_hours_list = EmployeeHours.objects.all().order_by('-date_added')

    if request.method == 'POST':

        form = EmployeeHoursForm(request.POST)

        if form.is_valid():
            employee_hours_item = EmployeeHours(
                employee=form.cleaned_data['employee'],
                hours=form.cleaned_data['hours'],
                overtime=form.cleaned_data['overtime'],
                task_description=form.cleaned_data['task_description'],
                task_number=form.cleaned_data['task_number'],
            )
            employee_hours_item.save()
            return HttpResponseRedirect('/budgetreport/summary/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EmployeeHoursForm()

    context = {
        'employee_hours_list': employee_hours_list,
        'form': form
    }

    return render(request,
                  'budgetreport/employee_hours.html',
                  context
                  )


# 3. Вкладка "Работа по должностям"
#   GET, POST
def employee_position_hours_view(request):
    additional_expenses = AdditionalExpenses.objects.all().order_by('-expense_value')
    position_hours = EmployeeHours.objects.values('employee__name',
                                                  'employee__position__position',
                                                  'employee__position__cost').annotate(total_hours=Sum('hours'))

    if request.method == 'POST':

        form = AdditionalExpensesForm(request.POST)

        if form.is_valid():
            additional_expenses_item = AdditionalExpenses(expense_purpose=form.cleaned_data['expense_purpose'],
                                                          expense_value=form.cleaned_data['expense_value'])
            additional_expenses_item.save()
            return HttpResponseRedirect('/budgetreport/employeepositionhours/')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = AdditionalExpensesForm()

    context = {
        'position_hours': position_hours,
        'additional_expenses': additional_expenses,
        'form': form
    }

    return render(request,
                  'budgetreport/employee_position_hours.html',
                  context
                  )


# 4. Вкладка "Ставки"
#   GET

class EmployeePositionList(ListView):
    model = EmployeePosition
    extra_context = {
        'employees': Employee.objects.all().order_by('position')
    }

from django.shortcuts import render
from django.views.generic import ListView
from budgetreport.models import *
from .forms import AdditionalExpensesForm, EmployeeHoursForm
from django.http import HttpResponseRedirect
from django.db.models import Sum, Model, PositiveIntegerField


# 1. Главная страница отчёта - общая информация с вкладки экселя "Счёт заказчику"
#   + кнопки перехода на остальные вкладки
#   GET (видимо придется делать функцию либо добавлять в контекст новую инфу)

def budget_summary(request):
    employee_hours = EmployeeHours.objects.all()
    additional_expenses = AdditionalExpenses.objects.all().aggregate(Sum('expense_value'))

    total_hours_cost = 0
    total_hours_cost_discount = 0

    for x in employee_hours:
        total_hours_cost += int(x.hours_cost())
    total_hours_cost += additional_expenses.get('expense_value__sum')

    overall_cost = 0

    context = {
        'total_hours_cost': total_hours_cost,

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
    """
    SELECT
        eh.employee,
        ep.position,
        SUM(eh.hours),
        SUM(ep.cost)
    FROM EmployeeHours eh
        LEFT JOIN Employee e ON eh.employee = e.pk
        LEFT JOIN EmployeePosition ep ON e.position = ep.pk
    GROUP BY eh.employee, ep.position

    """
    additional_expenses = AdditionalExpenses.objects.all().order_by('-expense_value')
    position_hours = EmployeeHours.objects.values('employee__name', 'employee__position__position', 'employee__position__cost').annotate(total_hours=Sum('hours'))

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
#   GET - Готово


class EmployeePositionList(ListView):
    model = EmployeePosition
    extra_context = {
        'employees': Employee.objects.all().order_by('position')
    }



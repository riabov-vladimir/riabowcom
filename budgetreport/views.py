from django.shortcuts import render
from budgetreport.models import *


def budget_summary(request):

    employees = Employee.objects.all().order_by('position')
    positions = EmployeePosition.objects.all().order_by('position')
    additional_expences = AdditionalExpences.objects.all().order_by('-expense_value')

    context = {
        'employees': employees,
        'positions': positions,
        'additional_expences': additional_expences
    }

    return render(request,
                  'budgetreport/budget_summary.html',
                  context
                  )

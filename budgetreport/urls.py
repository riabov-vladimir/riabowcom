from django.urls import path, include
from budgetreport.views import *


urlpatterns = [
    path('summary/', budget_summary, name='summary'),
    path('employeeposition/', EmployeePositionList.as_view(), name='employeeposition'),
    path('employeehours/', employee_hours_view, name='employeehours'),
]

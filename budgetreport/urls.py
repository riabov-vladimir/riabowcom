from django.urls import path, include
from budgetreport.views import *


urlpatterns = [
    path('summary/', budget_summary, name='summary'),
    # path('summary/<int:month>/<int:year>', budget_summary_period, name='summarybyperiod'),
    path('employeeposition/', EmployeePositionList.as_view(), name='employeeposition'),
    path('employeehours/', employee_hours_view, name='employeehours'),
    path('employeepositionhours/', employee_position_hours_view, name='employeepositionhours')
]

from django.urls import path, include
from budgetreport.views import budget_summary


urlpatterns = [
    path('summary/', budget_summary, name='summary')
]

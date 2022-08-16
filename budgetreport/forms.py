from django.forms import ModelForm, Form, CharField, IntegerField
from .models import EmployeeHours


class AdditionalExpensesForm(Form):
    expense_purpose = CharField(max_length=100, label='статья расходов')
    expense_value = IntegerField(label='сумма')


class EmployeeHoursForm(ModelForm):
    class Meta:
        model = EmployeeHours
        fields = ['employee', 'hours', 'overtime', 'task_description', 'task_number']
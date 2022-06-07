from django import forms


class AdditionalExpensesForm(forms.Form):
    expense_purpose = forms.CharField(max_length=100, label='статья расходов')
    expense_value = forms.IntegerField(label='сумма')

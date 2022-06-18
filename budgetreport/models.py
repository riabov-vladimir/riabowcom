from django.db import models


class EmployeePosition(models.Model):
    position = models.CharField(max_length=100, blank=False, null=True, verbose_name='специальность')
    cost = models.PositiveIntegerField(blank=False, null=True, verbose_name='ставка')
    cost_discount = models.PositiveIntegerField(blank=False, null=True, verbose_name='ставка со скидкой')
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.position} - {self.cost}'

    class Meta:
        verbose_name = 'компетенция'
        verbose_name_plural = 'компетенции'
        ordering = ['-cost']


class Employee(models.Model):
    name = models.CharField(max_length=50, blank=False, null=True, verbose_name='ФИО')
    position = models.ForeignKey(to=EmployeePosition, on_delete=models.CASCADE, verbose_name='специальность')
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'сотрудник'
        verbose_name_plural = 'сотрудники'
        ordering = ['position']


class AdditionalExpenses(models.Model):
    expense_purpose = models.CharField(max_length=100, blank=False, null=True, verbose_name='статья расходов')
    expense_value = models.IntegerField(blank=False, null=True, verbose_name='сумма')
    last_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.expense_purpose

    class Meta:
        verbose_name = 'дополнительные расходы'
        verbose_name_plural = 'дополнительные расходы'
        ordering = ['-expense_value']


class CurrentRdTeam(models.Model):
    employee = models.ForeignKey(to=Employee, on_delete=models.DO_NOTHING)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'участник команды'
        verbose_name_plural = 'участники команды'


class EmployeeHours(models.Model):
    employee = models.ForeignKey(to=Employee, on_delete=models.DO_NOTHING, verbose_name='сотрудник')
    hours = models.PositiveSmallIntegerField(null=False, verbose_name='часов списано')
    overtime = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='овертайм')
    task_description = models.CharField(blank=False, null=True, max_length=200, verbose_name='описание задачи')
    task_number = models.PositiveIntegerField(blank=True, null=True, verbose_name='номер задачи')
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.date_added} - {self.employee} - {self.task_description} - {self.hours} ч'

    class Meta:
        verbose_name = 'списанные часы'
        verbose_name_plural = 'списанные часы'
        ordering = ['-date_added']
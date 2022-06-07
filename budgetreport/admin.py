from django.contrib import admin
from .models import *


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeePosition)
class EmployeePositionAdmin(admin.ModelAdmin):
    pass


@admin.register(EmployeeHours)
class EmployeeHoursAdmin(admin.ModelAdmin):
    pass


@admin.register(AdditionalExpenses)
class AdditionalExpencesAdmin(admin.ModelAdmin):
    pass


@admin.register(CurrentRdTeam)
class CurrentRdTeamAdmin(admin.ModelAdmin):
    pass
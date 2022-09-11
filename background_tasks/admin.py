from django.contrib import admin
from .models import WeatherQuery


@admin.register(WeatherQuery)
class WeatherQueryAdmin(admin.ModelAdmin):
    readonly_fields = ('query_date',)

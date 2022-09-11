from django.contrib import admin
from django.forms import TextInput, Textarea, DateTimeField
from .models import WeatherQuery, PollutionQuery
from django.db import models


@admin.register(WeatherQuery)
class WeatherQueryAdmin(admin.ModelAdmin):
    readonly_fields = ('query_date',)
    list_display = ('weather_query_id',
                    'http_status_code',
                    'weather_state',
                    'temperature',
                    'pressure',
                    'humidity',
                    'cloudiness',
                    'wind_speed')  # tuple([f.name for f in WeatherQuery._meta.get_fields()]) = ALL FIELDS DISPLAYED
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


@admin.register(PollutionQuery)
class PollutionQueryAdmin(admin.ModelAdmin):
    readonly_fields = ('query_date',)
    list_display = ('pollution_query_id',
                    'http_status_code',
                    'air_quality_index',
                    'calc_date')   # tuple([f.name for f in WeatherQuery._meta.get_fields()]) = ALL FIELDS DISPLAYED
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '100'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})}
    }

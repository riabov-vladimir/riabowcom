from django.contrib import admin
from django.forms import TextInput, Textarea, DateTimeField
from .models import WeatherQuery, PollutionQuery
from django.db import models


@admin.register(WeatherQuery)
class WeatherQueryAdmin(admin.ModelAdmin):
    readonly_fields = ('query_date',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
    }


@admin.register(PollutionQuery)
class PollutionQueryAdmin(admin.ModelAdmin):
    readonly_fields = ('query_date',)
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size':'100'})},
        models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})}
    }

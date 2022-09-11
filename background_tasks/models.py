from django.db import models


class WeatherQuery(models.Model):
    """
    API documentation https://openweathermap.org/api
    Data source - GET request to http://api.openweathermap.org/data/2.5/weather?id={apiKey}&units=metric&lang=ru
    """
    weather_query_id = models.AutoField(primary_key=True, verbose_name='Идентификатор запроса')
    query_response_body_raw = models.CharField(blank=True, max_length=1000, verbose_name='Ответ на запрос')
    http_status_code = models.PositiveSmallIntegerField(verbose_name='Код ошибки')
    http_status_reason = models.CharField(max_length=1000, verbose_name='Текст ошибки')
    query_date = models.DateTimeField(auto_now_add=True, verbose_name='Время и дата запроса') # format = 2022-09-11 01:33:01.891463+00:00

    def parse(self):
        # TODO: add fields and write a code that would fill them from raw data field
        pass

    def __str__(self):
        return f'Weather#{self.pk}@{str(self.query_date)[0:-16]}'


class PollutionQuery(models.Model):
    """
    API documentation https://openweathermap.org/api/air-pollution
    Data source - GET request to http://api.openweathermap.org/data/2.5/weather?id={apiKey}&units=metric&lang=ru
    """
    pollution_query_id = models.AutoField(primary_key=True, verbose_name='Идентификатор запроса')
    query_response_body_raw = models.CharField(blank=True, max_length=1000, verbose_name='Ответ на запрос')
    http_status_code = models.PositiveSmallIntegerField(verbose_name='Код ошибки')
    http_status_reason = models.CharField(max_length=1000, verbose_name='Текст ошибки')
    query_date = models.DateTimeField(auto_now_add=True, verbose_name='Время и дата запроса') # format = 2022-09-11 01:33:01.891463+00:00

    def parse(self):
        # TODO: add fields and write a code that would fill them from raw data field
        pass

    def __str__(self):
        return f'Pollution#{self.pk}@{str(self.query_date)[0:-16]}'

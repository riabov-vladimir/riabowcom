import datetime
from django.db import models
import json


class WeatherQuery(models.Model):
    """
    API documentation - https://openweathermap.org/current#parameter
    Data source - GET request to http://api.openweathermap.org/data/2.5/weather?id={apiKey}&units=metric&lang=ru
    Classifications - https://openweathermap.org/weather-conditions
    """
    weather_query_id = models.AutoField(primary_key=True, verbose_name='Идентификатор запроса')
    query_response_body_raw = models.CharField(blank=True, max_length=1000, verbose_name='Ответ на запрос')
    http_status_code = models.PositiveSmallIntegerField(verbose_name='Код ошибки')
    http_status_reason = models.CharField(max_length=1000, verbose_name='Текст ошибки')
    query_date = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Время и дата запроса')  # format = 2022-09-11 01:33:01.891463+00:00
    # -------- geographic info ------ #
    calc_date = models.DateTimeField(null=True, verbose_name='Время и дата формирования данных')
    country_code = models.CharField(max_length=2, null=True, verbose_name='Код страны')
    sunrise = models.DateTimeField(null=True, verbose_name='Время восхода')
    sunset = models.DateTimeField(null=True, verbose_name='Время заката')
    timezone = models.PositiveIntegerField(null=True, verbose_name='Разница с UTC, с')
    city_id = models.IntegerField(null=True, verbose_name='Идентификатор города')
    city_name = models.CharField(max_length=200, null=True, verbose_name='Город')
    longitude = models.FloatField(null=True, verbose_name='Долгота')
    lattitude = models.FloatField(null=True, verbose_name='Широта')
    # ------ weather ------- #
    weather_state = models.CharField(max_length=50, null=True, verbose_name='Погода (кратко)')
    weather_description = models.CharField(max_length=200, null=True, verbose_name='Погода (подробно)')
    weather_icon = models.CharField(max_length=3, null=True,
                                    verbose_name='Погода (код изображения)')  # graphic icon code: 2 digits = id, letter n\d = day\night
    temperature = models.PositiveSmallIntegerField(null=True, verbose_name='Температура, С°')
    temp_min = models.PositiveSmallIntegerField(null=True, verbose_name='Минимальная температура, С°')
    temp_max = models.PositiveSmallIntegerField(null=True, verbose_name='Максимальная температура, С°')
    feels_like_temperature = models.PositiveSmallIntegerField(null=True, verbose_name='Ощущается как, С°')
    pressure = models.PositiveSmallIntegerField(null=True, verbose_name='Давление')
    pressure_sea_level = models.PositiveSmallIntegerField(null=True, verbose_name='Давление на уровне моря')
    pressure_ground_level = models.PositiveSmallIntegerField(null=True, verbose_name='Давление на уровне земли')
    humidity = models.PositiveSmallIntegerField(null=True, verbose_name='Влажность, %')
    visibility = models.PositiveSmallIntegerField(null=True, verbose_name='Дистанция видимости, м')
    wind_speed = models.PositiveSmallIntegerField(null=True, verbose_name='Скорость ветра, м/с')
    wind_direction = models.PositiveSmallIntegerField(null=True, verbose_name='Направление ветра (откуда), градусы')
    wind_gust = models.PositiveSmallIntegerField(null=True, verbose_name='Порывы ветра, м/с')
    cloudiness = models.PositiveSmallIntegerField(null=True, verbose_name='Облачность, %')
    # ---- rainfall amount last 1\3h
    rain_1h = models.PositiveSmallIntegerField(null=True, verbose_name='Осадки: Дождь, мм за 1 час')
    rain_3h = models.PositiveSmallIntegerField(null=True, verbose_name='Осадки: Дождь, мм за 3 часа')
    # ---- snowfall amount last 1\3h
    snow_1h = models.PositiveSmallIntegerField(null=True, verbose_name='Осадки: Снег, мм за 1 час')
    snow_3h = models.PositiveSmallIntegerField(null=True, verbose_name='Осадки: Снег, мм за 3 часа')

    def parse(self):
        data = json.loads(str(self.query_response_body_raw))
        # ------ data calc datetime ------- #
        dt = data.get('dt')
        self.calc_date = datetime.datetime.fromtimestamp(dt, datetime.timezone.utc) if dt else None
        # ------- sunrise\sunset datetime ----------#
        sunrise = data.get('sys', {}).get('sunrise')
        if sunrise:
            self.sunrise = datetime.datetime.fromtimestamp(sunrise, datetime.timezone.utc)
        # ------- sunset datetime ----------#
        sunset = data.get('sys', {}).get('sunset')
        if sunset:
            self.sunset = datetime.datetime.fromtimestamp(sunset, datetime.timezone.utc)

        self.country_code = data.get('sys', {}).get('country')
        self.timezone = data.get('timezone')
        self.city_id = data.get('id')
        self.city_name = data.get('name')
        # ------ coord --------- #
        self.longitude = data.get('coord', {}).get('lon')
        self.lattitude = data.get('coord', {}).get('lat')
        # ------ weather summary ------- #
        self.weather_state = data.get('weather', {})[0].get('main')
        self.weather_description = data.get('weather', {})[0].get('description')
        self.weather_icon = data.get('weather', {})[0].get('icon')
        # -------------- temperature ---------------#
        self.temperature = data.get('main', {}).get('temp')
        self.temp_min = data.get('main', {}).get('temp_min')
        self.temp_max = data.get('main', {}).get('temp_max')
        self.feels_like_temperature = data.get('main', {}).get('feels_like')
        # -------------- pressure ---------------#
        self.pressure = data.get('main', {}).get('pressure')
        self.pressure_sea_level = data.get('main', {}).get('sea_level')
        self.pressure_ground_level = data.get('main', {}).get('grnd_level')
        # -------------- mist\fog ---------------#
        self.humidity = data.get('main', {}).get('humidity')
        self.visibility = data.get('visibility')
        # -------------- wind ---------------#
        self.wind_speed = data.get('wind', {}).get('speed')
        self.wind_direction = data.get('wind', {}).get('deg')
        self.wind_gust = data.get('wind', {}).get('gust')
        # -------------- clouds ---------------#
        self.cloudiness = data.get('clouds').get('all')
        # ---- rainfall amount last 1\3h --------#
        self.rain_1h = data.get('rain', {}).get('1h')
        self.rain_3h = data.get('rain', {}).get('3h')
        # ---- snowfall amount last 1\3h --------#
        self.snow_1h = data.get('snow', {}).get('1h')
        self.snow_3h = data.get('snow', {}).get('3h')

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
    query_date = models.DateTimeField(auto_now_add=True,
                                      verbose_name='Время и дата запроса')  # format = 2022-09-11 01:33:01.891463+00:00

    def parse(self):
        # TODO: add fields and write a code that would fill them from raw data field
        pass

    def __str__(self):
        return f'Pollution#{self.pk}@{str(self.query_date)[0:-16]}'

import requests
from riabowcom.settings_local import WEATHER_API_KEY, CITY_ID, LON, LAT
from background_tasks.models import WeatherQuery, PollutionQuery
from datetime import datetime

"""
Run this command to add all defined jobs from CRONJOBS to crontab (of the user which you are running this command with):
    python manage.py crontab add  -- activates every cronjob  within CRONJOBS list @settings.py 
show current active jobs of this project:
    python manage.py crontab show
removing all defined jobs is straight forward:
    python manage.py crontab remove
"""


def weather_task():
    """
    A regular scheduled background task which calls OPENWEATHER API current weather method.

    Request example - http://api.openweathermap.org/data/2.5/weather?id={CITY_ID}&APPID={WEATHER_API_KEY}&units=metric&lang=ru
    - It's always better to pass settlement ID then it's name. The url-parameter is "id".
    - I'm using metric units for this app. The url-parametr is "units".
    - I wanna see verbose weather evaluations in russian. The url-parametr is "lang".
    :return:
    """

    # -------------- check if task works ---------------------
    # with open('crontab_journal.log', 'a', encoding='utf-8') as file:
    #     file.write(f'task start at {datetime.now()} \n')
    # --------------------------------------------------------

    query = requests.get(
        f'http://api.openweathermap.org/data/2.5/weather?id={CITY_ID}&APPID={WEATHER_API_KEY}&units=metric&lang=ru')
    weather_query = WeatherQuery(
        query_response_body_raw=query.text,
        http_status_code=query.status_code,
        http_status_reason=query.reason
    )
    try:
        weather_query.parse()
    except Exception as e:
        with open('crontab_journal.txt', 'a', encoding='utf-8') as file:
            file.write(f'task failed at {datetime.now()} with the following exception: {e} \n')

    weather_query.save()

    # -------------- check if task works ---------------------
    # with open('crontab_journal.log', 'a', encoding='utf-8') as file:
    #     file.write(f'task finish at {datetime.now()} \n')
    # --------------------------------------------------------


def pollution_task():
    """
    A regular scheduled background task which calls OPENWEATHER API air_pollution method.

    Request example - http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API key}
    :return:
    """
    query = requests.get(
        f'http://api.openweathermap.org/data/2.5/air_pollution?lat={LAT}&lon={LON}&appid={WEATHER_API_KEY}')
    pollution_query = PollutionQuery(
        query_response_body_raw=query.text,
        http_status_code=query.status_code,
        http_status_reason=query.reason
    )
    pollution_query.parse()
    pollution_query.save()

import requests
from riabowcom.settings_local import WEATHER_API_KEY
from background_tasks.models import WeatherQuery
from datetime import datetime


def weather_task():
    """
    Run this command to add all defined jobs from CRONJOBS to crontab (of the user which you are running this command with):
        python manage.py crontab add
    show current active jobs of this project:
        python manage.py crontab show
    removing all defined jobs is straight forward:
        python manage.py crontab remove
    :return:
    """

    # -------------- check if task works ---------------------
    # with open('test_task.txt', 'a', encoding='utf-8') as file:
    #     file.write(f'task start at {datetime.now()} \n')
    # --------------------------------------------------------

    query = requests.get(f'http://api.openweathermap.org/data/2.5/weather?id={WEATHER_API_KEY}&units=metric&lang=ru')
    weather_query = WeatherQuery.objects.create(
        query_response_body_raw=query.text,
        http_status_code=query.status_code,
        http_status_reason=query.reason
    )
    weather_query.parse()
    weather_query.save()

    # -------------- check if task works ---------------------
    # with open('test_task.txt', 'a', encoding='utf-8') as file:
    #     file.write(f'task finish at {datetime.now()} \n')
    # --------------------------------------------------------

from django.urls import path
from background_tasks.views import test
from main.views import *


urlpatterns = [
	path('', IndexView.as_view(), name='index'),
	path('cv', CvView.as_view(), name='cv'),
	# path('test', test, name='test'),  #         <<<----- url for testing
	path('cat', CatView.as_view(), name='cat')
]

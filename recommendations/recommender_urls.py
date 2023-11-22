
# different url for recommender engine
from django.urls import path
from . import api_view
urlpatterns = [
    path('get_infos', api_view.get_infos, name='get_anime_infos'),
    path('similar', api_view.get_similar, name='get_similar'),
]

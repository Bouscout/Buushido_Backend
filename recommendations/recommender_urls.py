
# different url for recommender engine
from django.urls import path
from . import api_view
from . import seach_bar
urlpatterns = [
    path('get_infos', api_view.get_infos, name='get_anime_infos'),
    path('similar', api_view.get_similar, name='get_similar'),
    path('query', seach_bar.query_search, name='querying'),
    path('direct_query', seach_bar.direct_query, name='direct_querying'),
]

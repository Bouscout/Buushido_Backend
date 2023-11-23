# handle most api request for recommendation engine
from django.shortcuts import get_list_or_404

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from recommendations.serializer import Anime_Serializer
from recommendations.models import anime, cluster
from .recommendation_engine import Engine
import random

Recommender = Engine()
POPULAR_CLUSTER = 16
NUM_ELEMENTS = 30

@api_view(["GET"])
def get_infos(request):
    if "animes" not in request.GET :
        return Response("Include the parameters '?animes=...'", status=status.HTTP_400_BAD_REQUEST)

    animes = request.GET["animes"]
    animes = list(map(int, str(animes).split(",")))

    # series_obj = get_list_or_404(anime, id__in=animes)
    series_obj = [anime.objects.using("my_anime_db").get(id=x) for x in animes]
    series = Anime_Serializer(series_obj, many=True)

    return Response(series.data, status=status.HTTP_200_OK)

# request for some popular animes 
@api_view(["GET"])
def popular(request):
    random_choices = cluster.objects.get(id=POPULAR_CLUSTER).anime_set.all()
    random_choices = random.sample(list(random_choices), k=NUM_ELEMENTS)
    series = Anime_Serializer(random_choices, many=True)    
    return Response(series.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_similar(request):
    if "animes" not in request.GET :
        return Response("Include the parameters '?animes=...'", status=status.HTTP_400_BAD_REQUEST)
    
    if "black_list" in request.GET :
        black_list = request.GET["black_list"]
        black_list = list(map(int, str(black_list).split(",")))
    
    else : black_list = []

    
    animes = request.GET["animes"]
    animes = list(map(int, str(animes).split(",")))

    close, distance = Recommender.similar(animes, black_list)

    series = Anime_Serializer(close, many=True)

    for serie, dist in zip(series.data, distance) :
        serie["distance"] = dist

    return Response(series.data, status=status.HTTP_200_OK)

# if user force to get a recommendations without having an account
@api_view(["GET"])
def get_recommendations(request):
    pass


@api_view(["GET"])
def get_custom_recommendations(request):
    pass


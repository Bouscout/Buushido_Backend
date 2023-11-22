# handle most api request for recommendation engine
from django.shortcuts import get_list_or_404

from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

from recommendations.serializer import Anime_Serializer
from recommendations.models import anime
from .recommendation_engine import Engine

Recommender = Engine()

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
    
@api_view(["GET"])
def get_similar(request):
    if "animes" not in request.GET :
        return Response("Include the parameters '?animes=...'", status=status.HTTP_400_BAD_REQUEST)
    
    animes = request.GET["animes"]
    animes = list(map(int, str(animes).split(",")))

    close, distance = Recommender.similar(animes)

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


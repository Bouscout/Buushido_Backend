# this handling the different request option for the recommender system

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from contenu.serializer import video_serial
from contenu.models import video
from contenu.recommender_system.recommend import Recommender
from time import time
import json

model = Recommender()

# user provides informations and gets a recommendation
# we also provide back the informations we parsed from the user request in order to have the input values for 
# the predicitons
@api_view(["GET"])
def send_recommendations(request):    
    last_watched = []

    if "watched" in request.GET :
        last_watched = request.GET["watched"]
        last_watched = list(map(int, str(last_watched).split(",")))
        print("last watched is : ", [video.objects.get(id=x) for x in last_watched])

    start = time()
    recommended = model.recommend_shows(last_watched)
    runtime = time() - start

    # for now the recommender returns the series object but when we will implement the caching system
    # the recommender will only return the ids
    # serie = [get_object_or_404(video, pk=x) for x in recommended]
    videos = video_serial(recommended, many=True)
    data = {
        "series" : videos.data,
        "userParams" : request.GET["watched"],
        "runtime" : runtime,
    }

    return Response(data, status=status.HTTP_200_OK)

# for storing the observations
# would need to be upgraded if too many requests
@api_view(["POST"])
def post_label(request):
    if request.method == "POST" :
        posted_infos = json.loads(request.body.decode("utf-8"))

        # we get the user input params
        user_param = posted_infos["userParams"]

        series_w_label = posted_infos["serieLabels"] # dict {showId : label}

        def write_line(serie, label) :
            with open("contenu/recommender_system/logs/log.csv", "a") as fichier :
                text = f"\n{user_param},{serie},{label}"
                fichier.write(text)

        for serie, label in series_w_label.items() :
            write_line(serie, label)

        return Response(status=status.HTTP_202_ACCEPTED)

    else :
        return Response(status=status.HTTP_400_BAD_REQUEST)

# this handling the different request option for the recommender system

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from contenu.serializer import video_serial
from contenu.models import video
from contenu.recommender_system.recommend import Recommender
from time import time

model = Recommender()

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

    # serie = [get_object_or_404(video, pk=x) for x in recommended]
    videos = video_serial(recommended, many=True)
    data = {
        "series" : videos.data,
        "userParams" : "1,2,3,4,5,5,6,6",
        "runtime" : runtime,
    }

    return Response(data, status=status.HTTP_200_OK)

    

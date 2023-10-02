from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import permissions, status
from models import metrics
from rest_framework.response import Response
import datetime


# create a num of connections in the website with each new connection for user being counted every 6 hours
@api_view(['GET'])
def add_view(request):
    try :
        last_record = metrics.objects.latest('date')
    except :
        print()

    
# num of total user online

# num of people beign connected for brief moment

# average time spent on website

# make two names for anime
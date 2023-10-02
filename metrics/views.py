from django.shortcuts import render

# Create your views here.
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import permissions, status
from .models import WebTraffic, Not_brief_connection
from rest_framework.response import Response
import datetime
from contenu.models import video


# create a num of connections in the website with each new connection for user being counted every 6 hours
@api_view(['GET'])
def add_view(request):
    # print('the request info : ', request.META['HTTP_USER_AGENT'])
    msg = 'nothing'
    try :
        last_record = WebTraffic.objects.latest('date') # the entry for the day
    except :
        cas = WebTraffic.objects.create()
        cas.save(using='extra_db')
        print('object created')
        return Response('Object created successfully' ,status=status.HTTP_201_CREATED)
    
    
    last_time = last_record.date.date()
    now = timezone.now().date()
    print('now : ', now)
    print('last time : ', last_time)

    if now - last_time >= datetime.timedelta(days=1):
        new_entry = WebTraffic.objects.create(num_views_inTimeframe=1, user_info=str(request.META['HTTP_USER_AGENT']+'\n'))
        new_entry.save(using='extra_db')

        last_record = WebTraffic.objects.latest('date')

        # in case the num and date of brief connection is still calibrated on the last day
        if last_record.date > Not_brief_connection.objects.latest('date').date :
            cas = Not_brief_connection.objects.create(num_user_staying=0)
            cas.save(using='extra_db')

        print('new days ')
        msg = f'the num of views for {last_time} is : ' + str(last_record.num_views_inTimeframe)

    else :
        # incrementing the view 
        last_record.num_views_inTimeframe += 1
        
        last_record.user_info += str(request.META['HTTP_USER_AGENT'] + '|||||')
        last_record.save(using='extra_db')
        print('same day')
        msg = f'the num of views for {last_time} is : ' + str(last_record.num_views_inTimeframe)

    # print('last time : ', last_time)
    # print('last time_zone : ', now)

    return Response(msg, status=status.HTTP_200_OK)


    
# num of people beign connected for brief moment

# function for finding the num of user not leaving immediately
@api_view(['GET'])
def brief_user(request):
    msg = 'nothing'
    try :
        # finding the last record in the database
        last_record = Not_brief_connection.objects.latest('date')

    except :
        # creating the record for the first time
        cas = Not_brief_connection.objects.create()
        cas.save(using='extra_db')
        msg = 'Record created first time'
        return Response(msg, status=status.HTTP_201_CREATED)
    
    # checking the time difference and deciding if new record or old one
    now = timezone.now().date()
    last_time = last_record.date.date()

    # in case one day has passed create new record
    if now - last_time >= datetime.timedelta(days=1) :

        new_entry = Not_brief_connection.objects.create()
        new_entry.save(using='extra_db')

        # calibrating the date on the webtraffic one 
        
        last_record = Not_brief_connection.objects.latest('date')
        
        msg = f"the num of user not leaving directly for {last_record.date.date()} is : " + str(last_record.num_user_staying)

    else :
        last_record.num_user_staying += 1
        last_record.save(using='extra_db')
        msg = f"the num of user not leaving directly for {last_time} is : " + str(last_record.num_user_staying)

    return Response(msg, status=status.HTTP_200_OK)


# report for num of user leaving immediately
@api_view(['GET'])
def web_retention(request):
    msg = 'nothing'
    latest = WebTraffic.objects.latest('date')
    num_total = latest.num_views_inTimeframe
    extra_infos = latest.user_info
    num_staying = Not_brief_connection.objects.latest('date').num_user_staying

    num_user_leaving = num_total - num_staying

    retention = (num_staying * 100) / num_total
    retention = f"{retention:.2f}"

    msg = f"""For a total of {num_total} users, the num of users leaving immediatly is {num_user_leaving} so the web retention is : {retention}% (the higher the better)\n
    the user infos are : \n {extra_infos}"""
    
    return Response(msg, status=status.HTTP_200_OK)

# average time spent on website


# make two names for anime

# num of total user online
# 1 MB = 1048576 bytes
import sys
from contenu.serializer import episode_serializer
serie = video.objects.get(id=172)
episodes = serie.la_video_set.all()
serializer = episode_serializer(episodes, many=True)
redis_dict = {}
redis_dict[172] = serializer.data

@api_view(['GET'])
def test_redis(request):
    # serie = get_object_or_404(video, pk=id)
    result = redis_dict[172]
    return Response(result, status=status.HTTP_206_PARTIAL_CONTENT)
# from django.shortcuts import redirect
from django.urls import path
from . import views
urlpatterns = [
    path('webtraffic/', views.add_view, name='add_view'),
    path('brief_user/', views.brief_user, name='brief_user'),
    path('retention/', views.web_retention, name='retention'),
    path('test/', views.test_redis, name='test'),
        
]
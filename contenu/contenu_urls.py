from django.shortcuts import redirect
from django.urls import path
from . import views, view_serial
urlpatterns = [

    #links for old version of the website
    path('', views.maison,),
    path('home/', views.accueil, name='home'),
    path('home/<genre>', views.categorie, name='genre'),
    path('home/<int:id>/', views.page_serie, name='page_serie'),
    path('redirect/<genre>', views.rediriger_accueil, name='redirect'),
    path('home/<int:id>/<int:il>/', views.page_epi, name='page_episode'),
    path('home/<int:id>/<int:il>/<syntax>/', views.redirect_epi, name='redirect_epi'),
    path('home/tout/', views.voir_tout, name='tout'),
    path('redirect_serie/<int:id>', views.rediriger_serie, name='redirect_serie'),
    path('home/agenda/', views.agenda, name='agenda'),
    path('ajax/', views.recherche_ajaz, name='ajax'),
    path('ajax/<int:id>', views.ajax_redirect, name='ajax_redirect'),
    path('addwatch/', views.watchlist, name='add_watch'),


    #from this section the links are only api related
    path('api1/', view_serial.onglet_part1, name='api_test'),
    path('api2/', view_serial.onglet_part2, name='api_test2'),
    path('api3/', view_serial.onglet_part3, name='api_test3'),
    path('api/poster/', view_serial.poster, name='poster'),
    path('api/serie/<int:id>/', view_serial.accueil_serie, name='poster'),
    path('api/episode/<int:id>/', view_serial.only_episodes, name='only_episodes'),
    path('api/genre/<genre>/', view_serial.categorie, name='Categorie_serial'),
    path('api/all/', view_serial.see_all, name='see_all'),
    path('api/build/', view_serial.serie_build, name='all_series'),
    path('api/ajax/<search_name>/', view_serial.recherche_ajax, name='ajax_api'),
    
    


]
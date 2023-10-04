from django.shortcuts import redirect
from django.urls import path
from . import views, view_serial, recommender_view
urlpatterns = [
    # home page urls
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
    # path('apitest/', view_serial.testeur, name='api_testeur'),

    # recommendations urls
    path('api/recommendations', recommender_view.send_recommendations, name='send_recommendations'),
    path('api/post_label', recommender_view.post_label, name='post_label'),
    

    path('api1/', view_serial.onglet_part1, name='api_test'),
    path('api2/', view_serial.onglet_part2, name='api_test2'),
    path('api3/', view_serial.onglet_part3, name='api_test3'),
    path('api4/', view_serial.onglet_part4, name='api_test4'),
    path('api5/', view_serial.onglet_part5, name='api_test5'),
    path('api/onglet/<int:id>/', view_serial.get_onglet, name='get_onglet'),
    path('api6/', view_serial.special_onglet, name='onglet_special'),
    path('api/poster/', view_serial.poster, name='poster'),
    path('api/recent/', view_serial.recent_episodes, name='recent'),
    path('api/serie/<int:id>/', view_serial.accueil_serie, name='poster'),
    path('api/episode/<int:id>/', view_serial.only_episodes, name='only_episodes'),
    path('api/genre/<genre>/', view_serial.categorie, name='Categorie_serial'),
    path('api/all/', view_serial.see_all, name='see_all'),
    path('api/liste/<order>/', view_serial.liste_serie, name='liste_serie'),
    path('api/build/', view_serial.serie_build, name='all_series'),
    path('api/ajax/<search_name>/', view_serial.recherche_ajax, name='ajax_api'),

    # watchlist urls
    path('api/watchlist/', view_serial.watchlist.as_view(), name='watchlist_api'),
    path('api/watchlist/check/<int:id>/', view_serial.watch_check.as_view(), name='watchlist_check_api'),
    path('api/watchlist/update/<int:id>/', view_serial.add_watchlist.as_view(), name='watchlist_update_api'),
    
    


]
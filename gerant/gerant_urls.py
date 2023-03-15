from django.shortcuts import redirect
from django.urls import path
from . import views

#different in production
#code set up to allow web scrapper app built and shared to the authorized user to let the app do the CRUD operations for them
SECRET_CODE = 'hagdcdoebds5421542'
urlpatterns = [
    path('', views.accueil_gerant, name='gerant_accueil'),
    path('onglet/<int:id>/', views.edit_onglet, name='onglet_edit'),
    path('onglet/<int:id>/ordre/', views.ordre_serie, name='ordre_serie'),
    path('onglet/', views.create_onglet, name='onglet'),
    path('onglet/diffuse/', views.diffuser, name='diffusion'),
    path('onglet/diffuse/order', views.ordre_onglet, name='ordre_onglet'),
    path('serie/', views.poster_video, name='nouvelle_serie'),
    path('serie/<int:id>/', views.ajouter_plusieurs_episode, name='new_episodes'),
    path('serie/<int:id>/<int:il>/', views.modifier_lien, name='modifier_lien'),
    path('serie/plusieurs/<int:id>/', views.plusieurs_episodes, name='plusieurs'),
    path('edit/<int:id>/', views.modifier_serie, name='modifier_serie'),
    path('edit/<int:id>/epi/', views.supprim_episode, name='supprimer_epi'),
    path('serie/<int:id>/'+SECRET_CODE+'/', views.poste_auto, name='auto'),


]
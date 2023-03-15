from http.client import HTTPResponse
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from identifier.forms import formulaire_connection, formulaire_incription
from django.contrib.auth import authenticate, login, logout
from contenu.models import video

#to log in a user

def home_login(request):
    forms = formulaire_connection()
    message = 'welcome'
    if request.method == 'POST':
        forms = formulaire_connection(request.POST)
        if forms.is_valid():
            user = authenticate(
                username = forms.cleaned_data['username'],
                password = forms.cleaned_data['password'],
            )
            if user is not None :
                login(request, user)
                message = f"you made it {forms.cleaned_data['username']} congrats"
                return redirect('home')
            else :
                message = 'reessaie encore champion'
    template = loader.get_template('inscription.html')
    context = {
        'form':forms,
        'messahe':message,
    }
    #we will be able to edit the message in case we need to pass specific information to the user
    return HttpResponse(template.render(context, request))

#to sign up a user
def sign_up(request):
    forms = formulaire_incription()
    if request.method == 'POST':
        forms = formulaire_incription(request.POST)
        if forms.is_valid():
            user = forms.save()
            login(request, user)
            return redirect('watchlist', choix='choix')
    template = loader.get_template('inscription.html')
    context = {
        'forms':forms,
    }
    return HttpResponse(template.render(context, request))


# function for the user to select a few shows in order to predict its favorite genre
def add_watchlist(request, choix):
    videos = None
    genres = None
    if choix == 'choix':
        genres = ['Horreur', 'Sci-fi', 'Action', 'Aventure', "Mystere", 'Comedie','Drama', 'Romance', 'Slice of life', 'Seinen', 'Shonen', "Film", 'Isekai']
    else :
        choix = choix
        videos = video.objects.filter(genres__contains =str(choix))
    if request.method == 'POST':
        for elem in request.POST.getlist('lis'):
            if elem == 'None':
                continue
            s = elem[1:]
            request.user.anime_prefere.add(video.objects.get(id=s))
        return redirect('home')
    return render(request, 'watchlist.html', {'videos':videos, 'genres':genres})


#function for testing some new functionnalities   
def test(request):
    return render(request, 'maintenance.html')

    
# Create your views here.

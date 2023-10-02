from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory, modelformset_factory
from gerant.forms import onglet_serie , affichage_form, supprimer_onglet, formulaire_episode, formulaire_video, supprimer_episode, onglet_serie2
from .models import affichage, onglet
from contenu.models import video, la_video, films
from requests_html import HTMLSession
from gerant.utility_functions import is_allowed, set_saison_name

# reggroup all the views for all the CRUD operations accssible only for the admin

# home page for the different options of the admin page
def accueil_gerant(request):
    if not is_allowed(request=request):
        return redirect('home')
    videos = video.objects.all().order_by('name')
    return render(request, 'gerant.html', {'videos':videos})

# function to create an onglet with different shows
def create_onglet(request):
    if not is_allowed(request=request):
        return redirect('home')
    
    actual_onglet = onglet.objects.all()
    form = onglet_serie2(request.POST or None)
    if form.is_valid():
        ongle = onglet()
        ongle.save()
        ongle.name = form.cleaned_data['name']
        for elem in form.cleaned_data['onglet1']:
            ongle.onglet1.add(get_object_or_404(video, pk=elem))
            ongle.save()
    return render(request, 'onglet.html', {'form':form, 'onglets':actual_onglet})

# onglet to change the name or the shows of a given onglet
def edit_onglet(request, id):
    if not is_allowed(request=request):
            return redirect('home')
            
    cas = get_object_or_404(onglet, pk=id)
    form = onglet_serie(request.POST or None, instance=cas)
    supprim = supprimer_onglet()
    if request.method == 'POST':
        if 'editeur' in request.POST:
            if form.is_valid():
                form.save()
                #form.save()
        if 'supprimer' in request.POST:
            supprim = supprimer_onglet(request.POST or None)
            if supprim.is_valid():
                print('allez ca degage')
                cas.delete()
                return redirect('onglet')
                
    return render(request, 'onglet.html', {'form':form , 'supprim':supprim})

# function to change the order of the show in a given onglet
def ordre_serie(request, id):
    ongle = get_object_or_404(onglet, pk=id)
    series = ongle.onglet1.all()
    option = [x for x in range(1, len(series)+1)]
    if request.method == 'POST':
        liste = request.POST.getlist('choix')
        for x in range(len(liste)):
            obj = get_object_or_404(video, pk=int(liste[x]))
            obj.order_id = x+1
            obj.save()
        return redirect('onglet')
    return render(request, 'onglet.html', {'option':option, 'series':series})

# function to change the order of the onglet on the main page
def ordre_onglet(request):
    affiche = affichage.objects.all()[0]
    series = affiche.to_display.all()
    option = [x for x in range(1, len(series)+1)]
    if request.method == 'POST':
        liste = request.POST.getlist('choix')
        for x in range(len(liste)):
            obj = get_object_or_404(onglet, pk=int(liste[x]))
            obj.order_id = x+1
            obj.save()
        return redirect('onglet')
    return render(request, 'onglet.html', {'option':option, 'series':series})

#  function to handle all the changes in general to the main page
# concerning the onglets displayed or the posters at the top
def diffuser(request):
    if not is_allowed(request=request):
        return redirect('home')
    
    cas = affichage.objects.all()[0]
    form = affichage_form(request.POST or None)
    if form.is_valid():
        print('les premiers sont : ', form.cleaned_data['poster'][0])
        if form.cleaned_data['to_display'][0] != 'rien':
            cas.to_display.clear()
            for elem in form.cleaned_data['to_display'] :
                cas.to_display.add(get_object_or_404(onglet, pk=elem))
                cas.save()

        if form.cleaned_data['poster'][0] != 'rien' :
            cas.poster.clear()
            for elem in form.cleaned_data['poster'] :
                cas.poster.add(get_object_or_404(video, pk=elem))
                cas.save()
        return redirect('home')
    return render(request, 'onglet.html', {'form':form})

'''class MyArticleForm(formulaire_episode):
    def __init__(self, *args, user, **kwargs):
            self.user = user
            super().__init__(*args, **kwargs)'''


# initial function for adding episodes to a show
def ajouter_plusieurs_episode(request, id):
    if not is_allowed(request=request):
        return redirect('home')
    
    form4 = None
    serie = get_object_or_404(video, pk=id)

    #checking it the saisons have name in case we need to modify them
    if serie.saisons :
        saisons_name = serie.saisons
    else :
        saisons_name = None

    # if it has at least one episode we assume that we'll only need one form
    # maybe for a film of for an ongoing show episode
    if len(serie.la_video_set.all()) > 0 :
        #form = formulaire(queryset=serie.la_video_set.all())
        form = None
        form4 = formulaire_episode(request.POST or None)
    else:
        formulaire = formset_factory(formulaire_episode, extra=12)
        form = formulaire(request.POST or None)

    # in the case of a single form
    if form4 :
        if form4.is_valid():
            saison_num = request.POST['saison']
            new_saison_name = request.POST['saison_name']

            # checking if it is a film request
            is_film = request.POST.get('is_film', False)
            if is_film :
                special_name = new_saison_name
                url1 = form4.cleaned_data['url']
                url2 = form4.cleaned_data['url2']
                url3 = form4.cleaned_data['url3']

                # creating the film object and saving it
                movie = films.objects.create(
                    name=serie,
                    saison = saison_num,
                    special_name = special_name,
                    url = url1, 
                    url2 = url2 or None,
                    url3 = url3 or None,
                      )
                movie.save()

                # changing the status of the show
                if serie.has_film != True :
                    serie.has_film = True
                    serie.save()

                return redirect('gerant_accueil')

            else : # meaning it is for episodes
                # checking if we are setting a name for the saison
                if new_saison_name :
                    compact_name = set_saison_name(name=new_saison_name, saison_num=saison_num, actual=saisons_name)
                    if compact_name :
                        serie.saisons = compact_name
                        serie.save()
                
                vid= form4.save()
                vid.nom = serie
                vid.saison = saison_num
                vid.get_ref()
                vid.fullscreen()
                vid.save()
                return redirect('page_serie', id=id)

    # in the case of multiple forms
    if form :    
        if form.is_valid():
            saison_num = request.POST['saison']
            new_saison_name = request.POST['saison_name']

            # checking if it is a film
            is_film = request.POST.get('is_film', False)
            if is_film :
                special_name = new_saison_name
                url1 = form4.cleaned_data['url']
                url2 = form4.cleaned_data['url2'] or None
                url3 = form4.cleaned_data['url3'] or None

                # creating the film object and saving it
                movie = films.objects.create(
                    name=serie,
                    saison = saison_num,
                    special_name = special_name,
                    url = url1, 
                    url2 = url2 or None,
                    url3 = url3 or None,
                      )
                movie.save()

                 # changing the status of the show
                if serie.has_film != True :
                    serie.has_film = True
                    serie.save()
                
                return redirect('gerant_accueil')

            else : # meaning it is for episodes
                # checking if we are setting a name for the saison
                if new_saison_name :
                    compact_name = set_saison_name(name=new_saison_name, saison_num=saison_num, actual=saisons_name)
                    if compact_name :
                        serie.saisons = compact_name
                        serie.save()

                # setting the episode selected
                for cas in form:
                    if len(cas.cleaned_data) > 0 :
                        epi =cas.save()
                        epi.nom = serie
                        epi.saison = saison_num
                        epi.get_ref()
                        epi.fullscreen()
                        epi.save()
                        
            return redirect('page_serie', id=id)
    return render(request, 'postage.html', {'serie':serie, 'form':form, 'form4':form4 ,})

# function to force the presence of multiple form for adding episodes
def plusieurs_episodes(request, id):
    if request.user.is_anonymous:
        return redirect('home')
    elif request.user.is_friend != True:
        return redirect('home')
    serie = get_object_or_404(video, pk=id)
    formulaire = formset_factory(formulaire_episode, extra=12)
    form = formulaire(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            x = request.POST['saison']
            for cas in form:
                if len(cas.cleaned_data) > 0 :
                    print('alors cest :', cas.cleaned_data)
                    epi =cas.save()
                    epi.nom = serie
                    epi.saison = x
                    epi.get_ref()
                    epi.fullscreen()
                    epi.save()
            return redirect('page_serie', id=id)
    return render(request, 'postage.html', {'serie':serie, 'form':form})

# function to pposte a new show
def poster_video(request):
    if request.user.is_anonymous:
        return redirect('home')
    elif request.user.is_friend != True:
        return redirect('home')
    form = formulaire_video()
    if request.method == 'POST':
        form = formulaire_video(request.POST, request.FILES)
        if form.is_valid():
            vid= form.save(commit=False)
            vid.posteur = request.user
            vid.naming()
            vid.pic()
            vid.text()
            #vid.framing_links()
            vid.save()
            return redirect('new_episodes', id=vid.id)
    return render(request, 'postage.html', {'form2':form})

# function to edit a given show informations
def modifier_serie(request, id):
    if request.user.is_anonymous:
        return redirect('home')
    elif request.user.is_friend != True:
        return redirect('home')
    cas = get_object_or_404(video, pk=id)
    form = formulaire_video(instance=cas)
    form2 = supprimer_episode()
    if request.method == 'POST':
        form = formulaire_video(request.POST, request.FILES, instance=cas)
        if form.is_valid():
            vid= form.save(commit=False)
            vid.naming()
            vid.text()
            vid.pic()
            vid.save()
            return redirect('gerant_accueil')
        if 'supprimer' in request.POST:
            form2 = supprimer_episode(request.POST)
            if form2.is_valid():
                cas.delete()
                return redirect('gerant_accueil')
    return render(request, 'postage.html', {'form2':form, 'supprim':form2})

def supprim_episode(request, id):
    if request.user.is_anonymous:
        return redirect('home')
    elif request.user.is_friend != True:
        return redirect('home')
    cas = get_object_or_404(video, pk=id)
    videos = cas.la_video_set.all()
    form = supprimer_episode(request.POST or None)
    if request.method == 'POST':
        for elem in request.POST.getlist('episodes'):
            la_video.objects.get(id=int(elem)).delete()
    return render(request, 'postage.html', {'form3':form, 'video':videos})


def modifier_lien(request, id, il):
    serie = get_object_or_404(video, pk=id)
    form = formulaire_episode()
    if il > -1:
        epi = get_object_or_404(la_video, pk=il)
        form = formulaire_episode(request.POST or None, instance=epi)
    if form.is_valid():
        vid = form.save()
        vid.get_ref()
        vid.fullscreen()
        vid.save()
        return redirect('gerant_accueil')
    return render(request, 'postage.html', {'form5':form, 'serie':serie})
    
    
    
def poste_auto(request, id):
    serie = get_object_or_404(video, pk=id)

    # using large number of saisons
    formulaire = formset_factory(formulaire_episode, extra=500)
    form = formulaire(request.POST or None)
    is_film = False # making sure never post film through here

    if request.method == 'POST':
        if form.is_valid():
            saison_num = request.POST['saison']
            new_saison_name = request.POST['saison_name']
            if new_saison_name :
                # checking for previous saison set up
                saisons_name = serie.saisons or None

                # getting a compact string describing the saison
                compact_name = set_saison_name(name=new_saison_name, saison_num=saison_num, actual=saisons_name)
                
                # setting the saisons name
                if compact_name :
                    serie.saisons = compact_name
                    serie.save()

            for cas in form:
                if len(cas.cleaned_data) > 0 :
                    # print('alors cest :', cas.cleaned_data)
                    epi =cas.save()
                    epi.nom = serie
                    epi.saison = saison_num
                    epi.get_ref()
                    epi.fullscreen()
                    epi.save()
            return redirect('page_serie', id=id)
    return render(request, 'postage.html', {'serie':serie, 'form':form})


# function for an admin to parse out a link from a website
def link_parser(link):
    try :
        links = []
        session = HTMLSession()
        response = session.get(link)
        elements = response.html.find('iframe')
        if hasattr(elements, '__len__'):
            if len(elements) == 0:
                msg = 'Desole aucun lien trouve pour cette page :('
                return [True]
            else :
                for elem in elements :
                    try :
                        src = elem.attrs['src']
                        links.append(src)
                    except KeyError :
                        continue

        return links
    except :
        return [False]
        
def parser(request):
    # crowd control
    if request.user.is_anonymous:
        return redirect('home')
    elif request.user.is_friend != True:
        return redirect('home')
    
    final = [] # final response
    if request.method == 'POST':
        # method to find all links from request
        url = request.POST['lien']
        liens = link_parser(url)
        if liens[0] :
            if len(liens) > 0 :
                final = liens
            else :
                final = ['Desole aucun lien trouve :(']
        else :
            final = ["il semblerait qu'il y ait une erreur, veuillez contacter l'admin"]

        return render(request, 'parser.html', {'responses':final})
    
    # in case it is a get request
    return render(request, 'parser.html')

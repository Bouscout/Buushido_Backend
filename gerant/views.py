from django.shortcuts import render, get_object_or_404, redirect
from django.forms import formset_factory, modelformset_factory
from gerant.forms import onglet_serie , affichage_form, supprimer_onglet, formulaire_episode, formulaire_video, supprimer_episode, onglet_serie2
from .models import affichage, onglet
from contenu.models import video, la_video

#this is where all the CRUD operations are handled


#home page where only the authorized user are allower, should probably use django built in authentification system
def accueil_gerant(request):
    if request.user.is_anonymous:
        return redirect('home')
    elif request.user.is_friend != True:
        return redirect('home')
    videos = video.objects.all().order_by('name')
    return render(request, 'gerant.html', {'videos':videos})


#create a section with different selected shows
#this will be linked through a many to many relationship to different shows
def create_onglet(request):
    if request.user.is_friend != True:
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

#edit the shows selected in a section
def edit_onglet(request, id):
    if request.user.is_anonymous:
        return redirect('home')
    elif request.user.is_friend != True:
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



#define the order of the show in a selected section
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

#define the order of the different section in the home page
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


#allow to change the poster on the home page
def diffuser(request):
    if request.user.is_friend != True:
        return redirect('home')
    cas = affichage.objects.all()[0]
    form = affichage_form(request.POST or None)
    if form.is_valid():
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


#check if a show has any episodes then allow to add either one episode or 12
#this will always be linked to a given show through a one to many relationship
def ajouter_plusieurs_episode(request, id):
    if request.user.is_anonymous:
        return redirect('home')
    elif request.user.is_friend != True:
        return redirect('home')
    #formulaire = modelformset_factory(la_video, form=formulaire_episode, extra=5)
    form4 = None
    serie = get_object_or_404(video, pk=id)
    if len(serie.la_video_set.all()) > 0 :
        #form = formulaire(queryset=serie.la_video_set.all())
        form = None
        form4 = formulaire_episode(request.POST or None)
    else:
        formulaire = formset_factory(formulaire_episode, extra=12)
        form = formulaire(request.POST or None)
    if form4 :
        if form4.is_valid():
            a = request.POST['saison']
            vid= form4.save()
            vid.nom = serie
            vid.saison = a
            vid.get_ref()
            vid.fullscreen()
            vid.save()
            return redirect('page_serie', id=id)
    if form :    
        if form.is_valid():
            x = request.POST['saison']
            for cas in form:
                if len(cas.cleaned_data) > 0 :
                    epi =cas.save()
                    epi.nom = serie
                    epi.saison = x
                    epi.get_ref()
                    epi.fullscreen()
                    epi.save()
            return redirect('page_serie', id=id)
    return render(request, 'postage.html', {'serie':serie, 'form':form, 'form4':form4 ,})


#allow to add 12 more episodes to a show regardless if it already have episodes
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


#operation to post a new show with all of its attibutes and some class method to fill some other attributes
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
            vid.text()
            #vid.framing_links()
            vid.save()
            return redirect('new_episodes', id=vid.id)
    return render(request, 'postage.html', {'form2':form})


#edit the attributes of a show
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
            vid.save()
            return redirect('gerant_accueil')
        if 'supprimer' in request.POST:
            form2 = supprimer_episode(request.POST)
            if form2.is_valid():
                cas.delete()
                return redirect('gerant_accueil')
    return render(request, 'postage.html', {'form2':form, 'supprim':form2})

#delete episodes from a show
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


#operation to change the link of an episode in a given show
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
    
    
#operation for a web scrapper bot to post the episodes for one of the authorized user    
def poste_auto(request, id):
    serie = get_object_or_404(video, pk=id)
    formulaire = formset_factory(formulaire_episode, extra=48)
    form = formulaire(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            x = request.POST['saison']
            for cas in form:
                if len(cas.cleaned_data) > 0 :
                    epi =cas.save()
                    epi.nom = serie
                    epi.saison = x
                    epi.get_ref()
                    epi.fullscreen()
                    epi.save()
            return redirect('page_serie', id=id)
    return render(request, 'postage.html', {'serie':serie, 'form':form})

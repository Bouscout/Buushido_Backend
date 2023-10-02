from django.shortcuts import redirect, render, get_object_or_404
from gerant.models import affichage, calendrier
from contenu.models import video
from django.http import JsonResponse
import random
def maison(request):
    if request.user.is_anonymous:
        return render(request, 'maintenance.html')
    elif request.user.is_friend != True:
        return render(request, 'maintenance.html') 
    return redirect('redirect', genre='home')

def page_serie(request, id):
    ref = 'n'
    if request.user.is_anonymous:
        return render(request, 'maintenance.html')
    elif request.user.is_friend != True:
        return render(request, 'maintenance.html') 
    if request.user.is_anonymous:
        ref = 'n'
    elif get_object_or_404(video, pk=id) in request.user.anime_prefere.all() :
        ref = 'a'
    ref_id = id
    serie = get_object_or_404(video, pk=id)
    similaire = video.objects.filter(genre_1 = serie.genre_1 )
    similaires = set()
    for x in range(0, 10):
        a = random.randint(0, len(similaire)-1)
        similaires.add(similaire[a])
    episode = serie.la_video_set.all() or None
    try:
        saison = [x for x in range(1, (episode.latest('saison').saison)+1)]
    except AttributeError:
        return redirect('gerant_accueil')
    return render(request, 'page_serie.html', {'serie':serie , 'episodes':episode,  'saison':saison, 'ref':ref, 'ref_id':ref_id, 'similaires':similaires })

def page_epi(request, id, il):
    if request.user.is_anonymous:
        return render(request, 'maintenance.html')
    elif request.user.is_friend != True:
        return render(request, 'maintenance.html') 
    serie = get_object_or_404(video, pk=id)
    episode = serie.la_video_set.all() or None
    try:
        episode.get(ref = il)
    except :
        il = str(il)
        if il[-1] == '0':
            il = int(il[0]) -1
            il = str(il)+'1'
        else :
            il = int(il[0])+1
            il = str(il)+ '1'
        return redirect('page_episode', id=id, il=il)
    end = 0
    if il == episode[(len(episode))-1].ref :
        end = 2
    elif il == episode[0].ref :
        end = 3
    return render(request, 'page_episode.html', {'serie':serie , 'episodes':episode, 'id':il, 'end':end})

def categorie(request, genre):
    if request.user.is_anonymous:
        return render(request, 'maintenance.html')
    elif request.user.is_friend != True:
        return render(request, 'maintenance.html') 
    videos = video.objects.all()
    if genre == 'mylist':
        if request.user.is_anonymous:
            return redirect('login') 
        choix = 'Ma liste'
        videos = request.user.anime_prefere.all()
    else :
        choix = genre
        videos = video.objects.filter(genres__contains =str(choix))
    return render(request, 'categorie.html', {'videos':videos, 'nom':choix})


def accueil(request):
    if request.user.is_anonymous:
        return render(request, 'maintenance.html')
    elif request.user.is_friend != True:
        return render(request, 'maintenance.html') 
    affiche = affichage.objects.all()[0]
    onglets = []
    for onglet in affiche.to_display.all().order_by('order_id'):
        name = onglet.name
        onglet = onglet.onglet1.all().order_by('order_id')
        onglets.append([onglet, name])

    return render(request, 'page accueil.html', {'affiche':affiche, 'onglets':onglets, 'user':request.user})

def rediriger_accueil(request, genre):
    if genre == 'home' :
        return redirect('home')
    return redirect('genre', genre)

def rediriger_serie(request, id):
    print('on est la')
    return redirect('page_serie', id=id)


def redirect_epi(request, id, il, syntax):
    if syntax == 'previous':
        if str(il)=='110' :
            return redirect('page_episode', id=id, il=19)
        return redirect('page_episode', id=id, il=il-1)
    elif syntax == 'next':
        if str(il)=='19' :
            return redirect('page_episode', id=id, il=110)
        return redirect('page_episode', id=id, il=il+1)
    elif syntax == 'accueil':
        return redirect('page_serie', id)
    else :
        return redirect('page_episode', id=id, il=int(syntax))

liston = video()
dico = {}
indice = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
for x in indice:
    dico[x] = liston.search_value(x.upper()) 

def voir_tout(request):
    global dico
    return render(request, 'voir_tout.html', {'indice':indice, 'dico':dico,})

def agenda(request):
    agenda = calendrier.objects.all()
    return render(request, 'agenda.html', {'agenda':agenda})

class trienode:
    def __init__(self, word) :
        self.word = word
        self.child = {}
        self.is_end = False
class Trie :
    def __init__(self) :
        self.root = trienode('')
    def insert(self, word):
        node = self.root
        for f in word :
            if f in node.child:
                node = node.child[f]
            else :
                node.child[f] = trienode(f)
                node = node.child[f]
        node.is_end = True
    def adding(self, node, pre):
        if node.is_end == True :
            self.output.append((pre + node.word))
        for child in node.child.values():
            self.adding(child, pre + node.word)

    def search(self, pref):
        node = self.root
        for l in pref:
            if l in node.child:
                node = node.child[l]
            else : 
                return False
        self.output = []
        self.adding(node, pref[:-1])
        return self.output
        
# let's add all the data 
every = video.objects.all()
diconame = {}
tr = Trie()
for elem in every:
    diconame[elem.name]=elem.id
    tr.insert(str(elem.name))
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
def recherche_ajaz(request ):
    combi = []
    text = request.GET.get('text')
    # print('alors le text est : ', text)
    result = None
    if text:
        result = tr.search(text.capitalize())
        for i in range(len(result)):
            combi.append([result[i], diconame[result[i]]])
    if is_ajax(request=request):
        return JsonResponse({'seconds':combi}, status=200)
    return render(request, 'recherche.html')

def ajax_redirect(request, id):
    return redirect('page_serie', id=id)

def watchlist(request):
    text = request.GET.get('text')
    cas = get_object_or_404(video, pk=text)
    if is_ajax(request=request):
        if request.user.is_anonymous:
            return JsonResponse({'message':'Veuillez vous connecter'}, status=200)
        elif cas in request.user.anime_prefere.all():
            request.user.anime_prefere.remove(cas)
            return JsonResponse({'message':'Retiré'}, status=200)
        else :
            request.user.anime_prefere.add(cas)
            return JsonResponse({'message':'Ajouté'}, status=200)
        


# Create your views here.

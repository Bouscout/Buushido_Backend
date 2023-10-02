from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import permissions, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from contenu.serializer import video_serial, posterialiseur, detail_serie_serializer,\
    episode_serializer, categorie_serial, voir_tout_serial,\
    onglet_special, film_serializer, episode_info

from contenu.models import video, la_video
from gerant.models import affichage, onglet
from datetime import datetime, timedelta

from contenu.django_case import DB_cache_test

DAYS_DELTA = 5
START = datetime.now() - timedelta(days=DAYS_DELTA)
NUM_EPISODES_RECENT = 20

cache = DB_cache_test()
onglets = affichage.objects.all()[0].to_display.all().order_by('order_id')

#pour store le cas des onglets dans l'api cache
def pour_most_recent(end=datetime.now()):
    sample_episode = la_video.objects.filter(date__range=[START, end]).order_by("-id")[:NUM_EPISODES_RECENT]
    sample_episode = episode_info(sample_episode, many=True)


    for element in sample_episode.data :
        nom_id = element['nom']
        element['nom'] = get_object_or_404(video, pk=int(nom_id)).name

    return sample_episode.data

    


def pour_onglet_old(liste, first=False):
    to_send = []
    for onglet in liste:
        if first == True :
            videos = video_serial(onglet.onglet1.all().order_by('order_id'), many=True)
        else :
            videos = video_serial(onglet.onglet1.all().order_by('-note'), many=True)

        onglet_info = {
                'name' : onglet.name ,
                'description' : onglet.description_onglet,
                'link' : onglet.link_to,
            }
        to_send.append((onglet_info, videos.data))

    return to_send

def pour_onglet(id, first=False):
    id = int(id) - 1
    all_onglets = onglets
    if id == 20 :
        to_send = []
        selection = all_onglets[9:]
        for onglet in selection :
            if first == True :
                videos = video_serial(onglet.onglet1.all().order_by('order_id'), many=True)
            else :
                videos = video_serial(onglet.onglet1.all().order_by('note'), many=True)

            onglet_info = {
                'name' : onglet.name ,
                'description' : onglet.description_onglet,
                'link' : onglet.link_to,
            }
            to_send.append((onglet_info, videos.data))

        return to_send

    else : 
        try : 

            onglet = all_onglets[id]
            if first == True :
                videos = video_serial(onglet.onglet1.all().order_by('order_id'), many=True)
            else :
                videos = video_serial(onglet.onglet1.all().order_by('note'), many=True)

            onglet_info = {
                'name' : onglet.name ,
                'description' : onglet.description_onglet, 
                'link' : onglet.link_to,
            }
            to_send = (onglet_info, videos.data)

            return to_send
        except IndexError :
            return 'No onglet at this index'
        
# the last added shows



# for x in range(15):
#     x += 1
#     special_request = f"onglet-{x}"
#     cache.adding(special_request, pour_onglet(x))


# pour onglet special (the one with the )
def cache_special():
    cas = get_object_or_404(onglet, pk=13)
    videos = onglet_special(cas.onglet1.all(), many=True)
    print('special appelez')
    return videos.data



# pour les categories
def cache_categorie(genre):
    if genre == 'Film': 
        videos = video.objects.filter(has_film=True)
        serializer = categorie_serial(videos, many=True)
        print('the film')
        return serializer.data

    else : 
       videos = video.objects.filter(genres__contains = str(genre))
       serializer = categorie_serial(videos, many=True)
       return serializer.data





# pour les posters
def cache_posters():
    post = affichage.objects.all()[0].poster.all()
    serializer = posterialiseur(post, many=True)
    print('poster appelez')
    return serializer.data


# =================== All caching set up ===========================
# cache.adding('posters', cache_posters())


cache.adding('onglet1', pour_onglet_old(onglets[:2], first=True))
# cache.adding('onglet2', pour_onglet_old(onglets[2:4]))
# cache.adding('onglet3', pour_onglet_old(onglets[4:6]))
# cache.adding('onglet4', pour_onglet_old(onglets[6:8]))
# cache.adding('onglet5', pour_onglet_old(onglets[8:]))

cache.adding('recent', pour_most_recent())

# cache.adding('onglet_special', cache_special())

categorie = ['Action', 'Aventure', 'Mystere', 'Horreur', 'Isekai', 'Comedie', 'Fantaisie',
            'Shonen', 'Romance', 'Sci-fi', 'Ecchi', 'Drama', 'Seinen', 'Slice of life', 'Thriller',
            'Shojo', 'Classique', 'Film']

# for elem in categorie :
#     cache.adding(elem.lower(), cache_categorie(elem))


# =================== All caching set up ===========================

# all done but this is only for the test

@api_view(["GET"])
def recent_episodes(request):
    data = cache.handle("recent")
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])    
def onglet_part1(request):
    
    data = cache.handle('onglet1')
    return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)
    
    # to_send = []

    # if request.method == 'GET':
    #     onglets = affichage.objects.all()[0].to_display.all().order_by('order_id')

    #     for onglet in onglets[:2]:
    #         videos = video_serial(onglet.onglet1.all().order_by('order_id'), many=True)
    #         to_send.append((onglet.name, videos.data))

    #     return Response(to_send, status=status.HTTP_206_PARTIAL_CONTENT)


@api_view(['GET'])    
def onglet_part2(request):
    
    data = cache.handle('onglet2')
    return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)
    # to_send = []

    # if request.method == 'GET':
    #     onglets = affichage.objects.all()[0].to_display.all().order_by('order_id')

    #     for onglet in onglets[2:4]:
    #         videos = video_serial(onglet.onglet1.all().order_by('order_id'), many=True)
    #         to_send.append((onglet.name, videos.data))

    #     return Response(to_send, status=status.HTTP_206_PARTIAL_CONTENT)


@api_view(['GET'])    
def onglet_part3(request):
    
    data = cache.handle('onglet3')
    return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)
    # to_send = []
    # if request.method == 'GET':
    #     onglets = affichage.objects.all()[0].to_display.all().order_by('order_id')

    #     for onglet in onglets[4:6]:
    #         videos = video_serial(onglet.onglet1.all().order_by('order_id'), many=True)
    #         to_send.append((onglet.name, videos.data))

    #     return Response(to_send, status=status.HTTP_206_PARTIAL_CONTENT)

@api_view(['GET'])    
def onglet_part4(request):
    
    data = cache.handle('onglet4')
    return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)
    # to_send = []
    # if request.method == 'GET':
    #     onglets = affichage.objects.all()[0].to_display.all().order_by('order_id')

    #     for onglet in onglets[6:8]:
    #         videos = video_serial(onglet.onglet1.all().order_by('order_id'), many=True)
    #         to_send.append((onglet.name, videos.data))

    #     return Response(to_send, status=status.HTTP_206_PARTIAL_CONTENT)
    
@api_view(['GET'])
def onglet_part5(request):
    
    data = cache.handle('onglet5')
    return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)
    # to_send = []
    # if request.method == 'GET':
    #     onglets = affichage.objects.all()[0].to_display.all().order_by('order_id')

    #     for onglet in onglets[8:]:
    #         videos = video_serial(onglet.onglet1.all().order_by('order_id'), many=True)
    #         to_send.append((onglet.name, videos.data))

    #     return Response(to_send, status=status.HTTP_206_PARTIAL_CONTENT)
    
    
# for the "selection personelle tab"
@api_view(['GET'])
def special_onglet(request):
    
    data = cache.handle('onglet_special')
    return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)
    # cas = get_object_or_404(onglet, pk=13)
    # videos = onglet_special(cas.onglet1.all(), many=True)
    # return Response(videos.data, status=status.HTTP_206_PARTIAL_CONTENT)

@api_view(['GET'])
def get_onglet(request, id):
    special_request = f'onglet-{id}'
    data = cache.handle(special_request)
    print('onglet got got')
    return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)

    # id = int(id) - 1
    # all_onglets = affichage.objects.all()[0].to_display.all().order_by('order_id')
    # onglet = all_onglets[id]
    # videos = video_serial(onglet.onglet1.all().order_by('order_id'), many=True)
    # onglet_info = {
    #     'name' : onglet.name ,
    #     'description' : onglet.description_onglet
    # }
    # to_send = (onglet_info, videos.data)
    # return Response(to_send, status=status.HTTP_206_PARTIAL_CONTENT)


# data for the big poster
@api_view(['GET'])
def poster(request):
    
    data = cache.handle('posters')
    # print('was cached')
    return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)
    # if request.method == 'GET':
    #     post = affichage.objects.all()[0].poster.all()
    #     serializer = posterialiseur(post, many=True)
    #     return Response(serializer.data)

# all the series on the home page  
@api_view(['GET'])
def accueil_serie(request, id):
    try :
        serie = get_object_or_404(video, pk=id)
        serie_serial = detail_serie_serializer(serie)
        episodes = episode_serializer(serie.la_video_set.all(), many=True)

        # checking if the serie has film :
        films = serie.films_set.all()
        if films and len(films) > 0 :
            the_films = film_serializer(films, many=True)
            to_send = [serie_serial.data, episodes.data, the_films.data]

        else :
            to_send = [serie_serial.data, episodes.data]
            
        return Response(to_send, status=status.HTTP_206_PARTIAL_CONTENT)
    except :
        return Response(status=status.HTTP_204_NO_CONTENT)

# serie for displaying in categorie section
@api_view(['GET'])
def categorie(request, genre):
    
    data = cache.handle(str(genre).lower())
    # print('was cached cate')
    return Response(data, status=status.HTTP_206_PARTIAL_CONTENT)
    # videos = video.objects.filter(genres__contains = str(genre))
    # serializer = categorie_serial(videos, many=True)
    # return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

# getting all the show and placing them in order
@api_view(['GET'])
def see_all(request):
    indices = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    liston = video()
    couplet = []
    for elem in indices:
        videos = liston.search_value(elem.upper())
        data_v = voir_tout_serial(videos, many=True)
        couplet.append((elem, data_v.data))
    return Response(couplet, status=status.HTTP_206_PARTIAL_CONTENT)

#just to run some tests
@api_view(['GET'])
def serie_build(request):
    videos = video.objects.all()
    serializer = detail_serie_serializer(videos, many=True)
    return Response(serializer.data)

# in order to parse the serie from a list of submitted ids
@api_view(['GET'])
def liste_serie(request, order):
    order = order.split('|')
    series = []
    for elem in order :
        if elem == '<end>': break
        show = get_object_or_404(video, pk=int(elem))
        series.append(show)

    serializer = video_serial(series, many=True)
    return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)


#in order to get only the episodes of a show
@api_view(['GET'])
def only_episodes(request, id):
    serie = get_object_or_404(video, pk=id)
    episodes = serie.la_video_set.all()
    serializer = episode_serializer(episodes, many=True)
    return Response(serializer.data, status=status.HTTP_206_PARTIAL_CONTENT)

#I am going to use a prefix trie in combinaison with a dictionnary 
#for all shows name inserted in the trie, I will make a dictionnary with the key 
# corresponding to the name and value corresponding to the serialized data 

#then for the search, we'll use the trie to find the right name and then we'll return them using the dictionnary 


from contenu.prefix_trie import Trie
tr = Trie()
dico_with_name = {}
for elem in video.objects.all():
    tr.insert(str(elem.name).lower())
    serialized = detail_serie_serializer(elem)
    dico_with_name[str(elem.name).lower()] = serialized
    if elem.other_name :
        tr.insert(str(elem.other_name).lower())
        dico_with_name[str(elem.other_name).lower()] = serialized



@api_view(['GET'])
def recherche_ajax(request, search_name):
    final_results = []
    search = search_name
    
    #use this line in case the request is in POST method and set the api view to POST
    # search = request.data['text']

    #let's check for the special character '$' signaling that the research bar is empty
    #then we'll send an empty array
    if str(search) == '$' : return Response([])

    result = tr.search(str(search).lower())
    #we are just going to work with only first 5 results
    result = result[:5] if len(result) > 5 else result 
    
    #we'll catch an error if the Trie return false for search method
    try :
        final_results = [dico_with_name[serie].data for serie in result]
    except TypeError:
        return Response([], status=status.HTTP_204_NO_CONTENT)
    #old method using the database starts_with function, wasn't working properly
    # suggestions = video.objects.filter(name__startswith=str(search))
    # serializer = voir_tout_serial(suggestions, many=True)
    return Response(final_results, status=status.HTTP_206_PARTIAL_CONTENT)

# we will use this class to display all the shows in a watchlist
class watchlist(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request):
        liste = request.user.anime_prefere.all()
        liste.reverse()
        print(f'for the user {request.user} the shows are : ', liste)
        # we will return the shows if there is at least one of them
        if len(liste) > 0 :
            videos = categorie_serial(liste, many=True)

            return Response(videos.data, status=status.HTTP_206_PARTIAL_CONTENT)
        
        # in case there is no show we'll return a status for that case

        message = "Vous n'avez pas encore garni votre watchlist"
        return Response(message, status=status.HTTP_204_NO_CONTENT)

# we will use this class for request of adding or remeving a show from a watchlist
class add_watchlist(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, id) :

    
        user = request.user
        print('for ', user)
        serie = get_object_or_404(video, pk=id)
        print('the serie is : ', serie.name)

        #we can assume the user is always going to be connected otherwise uncomment this
        # if user.is_anonymous :
        #     print('no user')
        #     return Response(status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)

        if serie in user.anime_prefere.all() :
            
            user.anime_prefere.remove(serie)
            print('retirer')
            message = "retiré"
            return Response(message, status=status.HTTP_200_OK)
        
        else : 
            user.anime_prefere.add(serie)
            print('ajouter')
            message = 'ajouté'
            return Response(message, status=status.HTTP_201_CREATED)


# in order to check the presence of the show in the user        
class watch_check(APIView) : 
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, id):
        user = request.user
        serie = get_object_or_404(video, pk=id)

        if serie in user.anime_prefere.all() :
            message = True
            return Response(message, status=status.HTTP_200_OK)
        else : 
            message = False
            return Response(message, status=status.HTTP_200_OK)

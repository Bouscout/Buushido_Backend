from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from contenu.serializer import video_serial, posterialiseur, detail_serie_serializer, episode_serializer, categorie_serial, voir_tout_serial
from contenu.models import video
from gerant.models import affichage


#the fetch request for the elements of the first page has been divided into three part to allow to fetch them at different times if needed
@api_view(['GET'])    
def onglet_part1(request):
    to_send = []
    
    if request.method == 'GET':
        onglets = affichage.objects.all()[0].to_display.all()
    
        for onglet in onglets[:3]:
            videos = video_serial(onglet.onglet1.all(), many=True)
            to_send.append((onglet.name, videos.data))
        
        return Response(to_send)
    

@api_view(['GET'])    
def onglet_part2(request):
    to_send = []
   
    if request.method == 'GET':
        onglets = affichage.objects.all()[0].to_display.all()
   
        for onglet in onglets[3:7]:
            videos = video_serial(onglet.onglet1.all(), many=True)
            to_send.append((onglet.name, videos.data))
   
        return Response(to_send)


@api_view(['GET'])    
def onglet_part3(request):
    to_send = []
    
    if request.method == 'GET':
        onglets = affichage.objects.all()[0].to_display.all()
    
        for onglet in onglets[7:]:
            videos = video_serial(onglet.onglet1.all(), many=True)
            to_send.append((onglet.name, videos.data))

        return Response(to_send)

#for the posters on the main page
@api_view(['GET'])
def poster(request):
    if request.method == 'GET':
        post = affichage.objects.all()[0].poster.all()
        serializer = posterialiseur(post, many=True)
        return Response(serializer.data)

#home page of a selected show
@api_view(['GET'])
def accueil_serie(request, id):
    serie = get_object_or_404(video, pk=id)
    serie_serial = detail_serie_serializer(serie)
    episodes = episode_serializer(serie.la_video_set.all(), many=True)
    return Response([serie_serial.data, episodes.data])

#for selected categories
@api_view(['GET'])
def categorie(request, genre):
    videos = video.objects.filter(genres__contains = str(genre))
    serializer = categorie_serial(videos, many=True)
    return Response(serializer.data)

#for displaying all the shows with alphabetical indexes
@api_view(['GET'])
def see_all(request):
    indices = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    liston = video()
    couplet = []
    for elem in indices:
        videos = liston.search_value(elem.upper())
        data_v = voir_tout_serial(videos, many=True)
        couplet.append((elem, data_v.data))
    return Response(couplet)


#a fetch to all the availble show in case we need to build them as static pages
@api_view(['GET'])
def serie_build(request):
    videos = video.objects.all()
    serializer = detail_serie_serializer(videos, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def only_episodes(request, id):
    serie = get_object_or_404(video, pk=id)
    episodes = serie.la_video_set.all()
    serializer = episode_serializer(episodes, many=True)
    return Response(serializer.data)

#I am going to use a prefix trie in combinaison with a dictionnary 
#for all shows name inserted in the trie, I will make a dictionnary with the key 
# corresponding to the name and value corresponding to the serialized data 

#then for the search, we'll use the trie to find the right name and then we'll return them using the dictionnary 


from contenu.prefix_trie import Trie
tr = Trie()
dico_with_name = {}
for elem in video.objects.all():
    tr.insert(str(elem.name))
    dico_with_name[str(elem.name)] = detail_serie_serializer(elem)



@api_view(['GET'])
def recherche_ajax(request, search_name):
    final_results = []
    search = search_name
    
    #use this line in case the request is in POST method and set the api view to POST
    # search = request.data['text']

    #let's check for the special character '$' signaling that the research bar is empty
    #then we'll send an empty array
    if str(search) == '$' : return Response([])

    result = tr.search(str(search).capitalize())
    #we are just going to work with only first 5 results
    result = result[:5] if len(result) > 5 else result 
    
    #we'll catch an error if the Trie return false for search method
    try :
        final_results = [dico_with_name[serie].data for serie in result]
    except TypeError:
        return Response([])
    #old method using the database starts_with function, wasn't working properly
    # suggestions = video.objects.filter(name__startswith=str(search))
    # serializer = voir_tout_serial(suggestions, many=True)
    return Response(final_results)
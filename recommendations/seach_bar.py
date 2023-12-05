# handles anime name querying for search bar and others
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from contenu.prefix_trie import Trie
from recommendations.models import anime, cluster
from recommendations.serializer import Anime_Search_Serializer
import pickle

POPULAR_CLUSTER_ID = 18 # 11 also
LIMIT = 500
INIT_TRIE = True

tr = Trie()
dico_with_name = {}
Trie_file_path = "recommendations/saved/search_bar_trie/saved_trie.pkl"
Dico_file_path = "recommendations/saved/search_bar_trie/saved_dico.pkl"

def insert_result(serie:anime, serialized=None):
    name = str(serie.title).lower()
    # print("done : ", serie.index)
    tr.insert(name)
    serialized = serialized if serialized else Anime_Search_Serializer(serie).data
    dico_with_name[name] = serialized

def init_from_file():
    global tr, dico_with_name
    with open(Trie_file_path, "rb") as f:
        tr = pickle.load(f)

    with open(Dico_file_path, "rb") as f:
        dico_with_name = pickle.load(f)

    print("trie initialized from file")

def save_trie():
    with open(Trie_file_path, "wb") as f :
        pickle.dump(tr, f)
    with open(Dico_file_path, "wb") as f :
        pickle.dump(dico_with_name, f)
    
    print("all entries saved in trie")


def init_trie(list_animes):
    serialized = Anime_Search_Serializer(list_animes, many=True)
    for elem, serial in zip(list_animes, serialized.data):
        insert_result(elem, serial)

    print("search trie initialized")

#------------------- Initializing the search query ---------------------
if INIT_TRIE :
    init_from_file()
    # init_trie(
    #     cluster.objects.get(id=POPULAR_CLUSTER_ID).anime_set.all()
    # )

    # save_trie()
    # init_trie(anime.objects.all())



@api_view(["GET"])
def direct_query(request):
    if "query" not in request.GET :
        return Response("Include the parameters '?query=...'", status=status.HTTP_400_BAD_REQUEST)
    
    NUM_RESULTS = 5
    search = str(request.GET["query"]).capitalize()

    results =  anime.objects.filter(title__contains=search)
    serialized = Anime_Search_Serializer(results, many=True)

    for serie, serial in zip(results, serialized.data):
        insert_result(serie, serial)

    return Response(serialized.data, status=status.HTTP_200_OK) 





@api_view(["GET"])
def query_search(request):
    if "query" not in request.GET :
        return Response("Include the parameters '?query=...'", status=status.HTTP_400_BAD_REQUEST)
    
    # search process
    NUM_RESULTS = 5
    search = str(request.GET["query"]).lower()
    
    result = tr.search(search)

    # if there is no result
    if not isinstance(result, list) :
        return Response([], status=status.HTTP_204_NO_CONTENT)
    
    result = result[:NUM_RESULTS] if len(result) > NUM_RESULTS else result 

    # returning the results
    try :
        final_results = [dico_with_name[serie] for serie in result]
    except TypeError:
        return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(final_results, status=status.HTTP_200_OK)
    
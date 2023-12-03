# this class return all the shows similar to a certain points
from recommendations.models import anime, cluster
from .clustering import Cluster
import numpy as np

ANIME_DB = "my_anime_db"

class Vector_Space:
    def __init__(self, item_model) -> None:
        self.cluster = Cluster()
        self.cluster.load_cluster(file_path="recommendations/cluster_module/saves/anime_cluster.pickle")

        self.item_model = item_model # for latent vector predicitons

        self.num_neighbors = 2

    def get_vectors(self, animes:list, blacklist:list=[], fetched=False) -> np.ndarray:
        """
        Take in a list of ids and return their vector represensation in the vector space
        """
        if not fetched :
            animes = [anime.objects.using(ANIME_DB).get(id=x) for x in animes]
        
        vectors = []
        for x in animes :
            if x.features_vector and x.id not in blacklist:
                vectors.append(
                    np.frombuffer(x.features_vector, dtype=np.float32)
                )     
        vectors = np.array(vectors, dtype=np.float32).reshape(len(vectors), -1)
        return vectors


    def get_concat_vectors(self, vectors) -> np.ndarray:
        """
        Take in some vectors and concatenate them after passing through the item model
        """
        latent_vector = self.item_model(vectors)

        return np.concatenate([latent_vector, vectors], axis=-1)
    
    
    def find_cluster_elements(self, cluster_id, blacklist:list) -> list :
        """
        Takes in a cluster index and return a list of anime object.\n
        the elements in blacklist are omitted.
        """
        clust = cluster.objects.using(ANIME_DB).get(id=cluster_id) 
        return [x for x in clust.anime_set.all() if x.id not in blacklist]

    def distance_array(self, origin:np.ndarray, points:np.ndarray):
        """
        Returns the distance of all the points with respect to the origin
        """
        origin = np.tile(origin, (points.shape[0], 1))
        distances = np.sum(
            (origin - points) ** 2
        , axis=1)
        return distances
    
    def rank(self, item, rank_by, limit=50, desc=False) -> tuple:
        """
        Rank the elements by the passed value for a certain limit
        """
        pair = [(i, x) for i, x in zip(item, rank_by)]
        pair = sorted(pair, key=lambda x : x[1], reverse=desc)
        pair = pair[:limit]

        return ([x[0] for x in pair], [x[1] for x in pair])


    def find_close(self, ids:list, blacklist:list ,limit=30, fetched=False)  :
        """
        Given a list of animes ids, it returns a list of the closest one and a list of their distances
        """
        if not fetched :
            blacklist = blacklist + ids # elements to exclude
            center = self.get_concat_vectors(
                self.get_vectors(ids)
            )
        else :
            center = self.get_concat_vectors(ids) # we already have the animes vectors as ids

        center = np.mean(center, axis=0)
        close_cluster, centers = self.cluster.find_neighbors(center, num_neighbors=self.num_neighbors)

        animes = []
        for clust in close_cluster :
            animes += self.find_cluster_elements(clust+1, blacklist)

        candidats = self.get_vectors(animes, fetched=True)
        candidats = self.get_concat_vectors(candidats)
        distances = self.distance_array(center, candidats)

        # sorting the distances while preserving the ids
        animes, distances = self.rank(animes, rank_by=distances, limit=limit)

        return animes, distances


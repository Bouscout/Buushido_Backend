"""
This function handles retrieving the closest shows to a list of recently watched show provided
"""
import numpy as np
from contenu.models import video
from identifier.models import user_cluster
from contenu.models import cluster 
import pickle
from contenu.recommender_system.DeepLearningNumpy.network import network
from contenu.recommender_system.DeepLearningNumpy import Relu, linear

class UserParamsManager :
    def __init__(self, max_number=40, decay_rate=0.9) -> None:
        """
        max_number : max number of series that are going to composed the embedding\n

        decay_rate : decaying importance given to last recent passed shows
        """
        data_type = np.float32
        self.max_number = max_number

        self.decay_rate = decay_rate

        self.user_feat_dim = 64
        self.item_feat_dim = 64

        u_cluster = user_cluster.objects.all()
        
        self.user_centroid = np.array([np.frombuffer(x.centroid, dtype=data_type) for x in u_cluster])

        # predict the user parameters from the movies watched
        with open("contenu/recommender_system/model_parameters/user_latent_model.pickle", "rb") as fichier :
            self.model = network([128, 128, 64], "relu")
            params = pickle.load(fichier)
            activations = [Relu(), Relu(), linear()]
            self.model.load_model_with_params_from_tf(params, activations)

    def get_series_np(self, show_ids:list):
        """
        Get the features arrays from the shows id passed and return an array of all the features
        """
        show_params = []
        for id in show_ids :
            try :
                array_byte = video.objects.get(id=id).feature_array

                if array_byte :
                    array_byte = np.frombuffer(array_byte, dtype=np.float64)
                    show_params.append(array_byte)

            except ValueError :
                pass

        return np.array(show_params)


    def decaying_average(self, series_features) :
        num_series = len(series_features)

        decay_factor = np.array([self.decay_rate**x for x in range(num_series)]).reshape(-1, 1)

        series_features *= decay_factor

        return np.mean(series_features, axis=0)
    
    
    def find_user_cluster(self, shows_ids):
        all_features = self.get_series_np(shows_ids)
        user_feature = self.decaying_average(all_features)

        user_param = self.model(user_feature.reshape(1, -1))

        def distance(x, y) :
            distance = np.sum((x - y)**2)
            return distance
        
        found_cluster = None

        actual_distance = 100_000
        for cluster, center in enumerate(self.user_centroid) :
            dist = distance(center, user_param[0])
            if dist < actual_distance :
                found_cluster = cluster + 1
                actual_distance = dist

        return found_cluster, user_param
    
    def find_cluster_top_3(self, cluster_id):
        """
        Return the top 3 cluster where the users of this cluster are most likely to like the shows from
        """
        clust = user_cluster.objects.get(id=cluster_id)
        return [clust.fav_cluster_1, clust.fav_cluster_2, clust.fav_cluster_3]
    
    





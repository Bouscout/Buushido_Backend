

from contenu.models import video, cluster, special_cluster
from identifier.models import user_cluster
from contenu.recommender_system.DeepLearningNumpy.network import network
from contenu.recommender_system.DeepLearningNumpy.activations import Relu, linear, sigmoid
import numpy as np
import pickle

class SeriesFetcher:
    def __init__(self, num_recommendations=15) -> None:
        self.num_recommendations = num_recommendations

        # initializing the latent vector model
        with open("contenu/recommender_system/model_parameters/movie_latent_model.pickle", "rb") as fichier :
            params = pickle.load(fichier)
            self.latent_vector_model = network()
            activations = [Relu(), Relu(), linear()]
            self.latent_vector_model.load_model_with_params_from_tf(params, activations)
        
        # initializing the rating model
        with open("contenu/recommender_system/model_parameters/light_predictor_model.pickle", "rb") as fichier :
            params = pickle.load(fichier)
            self.rating_model = network()
            activations = [Relu(), Relu(), sigmoid()]
            self.rating_model.load_model_with_params_from_tf(params, activations)

        
        self.distribution = [45, 35, 20]

    def retrieve_series(self, video_cluster):
        clust = cluster.objects.get(id=video_cluster)
        videos = clust.all_videos()
        return videos
    
    def picks(self, top_3, user_vector , already_watched):
        """
        Pick the recommendations according to a distribution based on their cluster rankings
        """
        series_to_rank = []
        latent_vectors = []
        for cluster in top_3[:-1] :
            all_series = self.retrieve_series(cluster)
            for serie in all_series :
                if serie.id in already_watched :
                    continue
                
                if not serie.feature_array :
                    continue

                series_to_rank.append(serie)

                serie_vector = np.frombuffer(serie.feature_array, np.float64)
                serie_latent_vector = self.latent_vector_model(serie_vector.reshape(1, -1))

                concat_vector = np.concatenate([user_vector, serie_latent_vector], axis=-1)

                latent_vectors.append(concat_vector) 

        latent_vectors = np.array(latent_vectors)

        latent_vectors = latent_vectors[:, 0, :]

        ratings = self.rating_model(latent_vectors)

        series_to_rank = [(r, x) for r, x in zip(ratings, series_to_rank)]

        ranked_series = sorted(series_to_rank, key=lambda x: x[0], reverse=True)

        return ([x[1] for x in ranked_series[:self.num_recommendations]], [x[0] for x in ranked_series[:self.num_recommendations]])

                
    def picks_from_popular(self, max_attempt=100):
        """
        will return 15 unique elements if it finds enough unique elements within the specified number of iterations.
        If it cannot find 15 unique elements, it will return fewer than 15.
        """
        max_attempt = max_attempt
        pick_size = 5
        # we will pick 5 elements randomly from all three popular cluster :
        clusters = special_cluster.objects.all()

        picks = set()
        complete = False
        for _ in range(max_attempt) :
            if complete :
                return list(picks)[:15]
            
            for clust in clusters :
                videos = clust.videos.all()
                picks = picks.union(set(np.random.choice(videos, size=pick_size)))

                if len(picks) >= 15 :
                    complete = True
                    break

        return list(picks)
           




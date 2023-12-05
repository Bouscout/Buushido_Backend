# class handles the model responsible for the content_based_filtering
from typing import Any
from DeepLearningNumpy.network import network
import numpy as np

class Content_Based_filtering():
    def __init__(
            self, user_model_path:str, item_model_path:str, latent_model_path:str
    ) -> None:
        """
        Content Based filtering algorithm, takes in a user and item vector and output a compatibility latent vector of dim d
        """
        self.user_model = network()
        self.item_model = network()
        self.model = network()
        
        self.user_model.load_model(user_model_path)
        self.item_model.load_model(item_model_path)
        self.model.load_model(latent_model_path)

    def decaying_average(self, anime_feat:np.ndarray) -> np.ndarray :
        # decay_rate = 0.95
        decay_rate = 1
        num_series = anime_feat.shape[0]
        if num_series == 0:
            return np.zeros((anime_feat.shape[1]))

        decay_factor = np.array([decay_rate**x for x in range(num_series)]).reshape(-1, 1)

        anime_feat *= decay_factor
        return np.mean(anime_feat, axis=0)


    def user_features(self, watched_feature:np.ndarray, age:int=None, gender:str=None):
        if age is None : age = 18
        else : age = int(age)
        MIN_AGE = 12
        MAX_AGE = 70
        age_scaled = (age - MIN_AGE) / (MAX_AGE - MIN_AGE)

        info_vec = np.array([age_scaled, 0, 0, 0])
    
        if gender is not None :
            gender_encoding = {
                "male" : 1,
                "female" : 2,
                "non_binary" : 3,
            }
            info_vec[gender_encoding[gender.lower()]] = 1
        
        return np.concatenate([info_vec, watched_feature], axis=-1).reshape(1, -1)


    def predict(self, xu:np.ndarray, xi:np.ndarray):
        num_item = xi.shape[0]

        # we expand the user vector to the num of item
        xu = np.repeat(xu.reshape(1, -1), num_item, axis=0)

        # content model inference and normalization
        user_latent = self.user_model(xu)
        user_latent = user_latent / np.linalg.norm(user_latent, ord=2, axis=1, keepdims=True)

        item_latent = self.item_model(xi)
        item_latent = item_latent / np.linalg.norm(item_latent, ord=2, axis=1, keepdims=True)

        content_latent = self.model(np.concatenate([user_latent, item_latent], axis=-1))

        return content_latent

    def __call__(self, xu:np.ndarray, xi:np.ndarray) -> Any:
        return self.predict(xu, xi)
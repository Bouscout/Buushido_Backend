
from typing import Any
from DeepLearningNumpy.network import network
import numpy as np
from recommendations.utils import load_np_array

class Collab_Model():
    def __init__(self, model_path:str) -> None:
        """
        Collaborative filtering algorithm, takes in an idx or parameter for the anime and the user and return a latent rating vector
        """
        self.model = network()
        self.model.load_model(model_path)

        self.average_user_param = load_np_array("recommendations/saved/numpy_models/avg_user_param.pkl")
        
        self.item_params = load_np_array("recommendations/saved/numpy_models/item_collab_pair.pkl")

    def predict(self, anim_idx:list, user_param=None):
        if user_param is None :
            user_param = self.average_user_param

        anim_param = self.item_params[anim_idx]

        # expand the dimensions of the user
        user_param = np.repeat(user_param.reshape(1, -1), anim_param.shape[0], axis=0)

        latent_rating = self.model(np.concatenate([user_param, anim_param], axis=-1))
        return latent_rating

    def __call__(self, anim_idx:list, user_param=None) -> Any:
        return self.predict(anim_idx, user_param)
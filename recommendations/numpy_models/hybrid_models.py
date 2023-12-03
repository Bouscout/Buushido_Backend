from DeepLearningNumpy.network import network
from typing import Callable, Union
import numpy as np

cf_format = Callable[[np.ndarray, np.ndarray], np.ndarray]
clb_format = Callable[[list, Union[np.ndarray, None]], np.ndarray]

class Hybrid_Model():
    def __init__(self, model_path:str, cf:cf_format, clb:clb_format) -> None:
        """
        Makes a prediction of the rating based on the confidence given on either the content based filter or the collaborative filter
        """
        self.content_filter = cf 
        self.collab_filter = clb

        self.model = network()
        self.model.load_model(model_path)

    def predict(self, user_feat:np.ndarray, anim_feat:np.ndarray, user_param:Union[np.ndarray, None], item_idx:list, weights:tuple):
        cf_weight, clb_weight = weights

        # content filter prediction
        content_latent = self.content_filter(user_feat, anim_feat)
        content_latent = (content_latent / np.linalg.norm(content_latent, ord=2, axis=1, keepdims=True)) * cf_weight

        # collab predicition
        collab_latent = self.collab_filter(item_idx, user_param)
        collab_latent = (collab_latent / np.linalg.norm(collab_latent, ord=2, axis=1, keepdims=True)) * clb_weight

        ratings = self.model(content_latent + collab_latent)
        return ratings

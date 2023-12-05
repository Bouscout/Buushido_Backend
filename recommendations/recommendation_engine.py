from recommendations.cluster_module.vector_space import Vector_Space
from DeepLearningNumpy.network import network
from recommendations.numpy_models import Collab_Model, Content_Based_filtering, Hybrid_Model
import numpy as np
from django.shortcuts import get_list_or_404

class Engine:
    def __init__(self) -> None:
        self.content_model = Content_Based_filtering(
            user_model_path="recommendations/saved/numpy_models/content_user_model.pkl",
            item_model_path="recommendations/saved/numpy_models/content_item_model.pkl",
            latent_model_path="recommendations/saved/numpy_models/content_model.pkl",
        )

        self.collab_model = Collab_Model(model_path="recommendations/saved/numpy_models/collab_model.pkl")

        self.hybrid_model = Hybrid_Model(
            model_path="recommendations/saved/numpy_models/hybrid_model.pkl",
            cf=self.content_model, clb=self.collab_model
        )
        
        self.space = Vector_Space(self.content_model.item_model)

        self.embedding_size = 100 # when retrieval for ranking


    def similar(self, ids:list, blacklist:list):
        return self.space.find_close(ids, blacklist)
    
    def ranking_visitor(self, age:int, gender:str, animes:list, blacklist:list):
        user_param = None # visitor

        # get input vectors
        user_anim_features = self.space.get_vectors(animes, blacklist=blacklist)
        user_feat = self.content_model.decaying_average(user_anim_features)

        user_feat = self.content_model.user_features(user_feat, age, gender)

        # embedding retrieval
        blacklist = blacklist + animes
        animes_canditate, distance = self.space.find_close(user_anim_features, blacklist=blacklist, limit=self.embedding_size, fetched=True)
        animes_idx = [anim.index for anim in animes_canditate]
        animes_features = self.space.get_vectors(animes_canditate, fetched=True)
        
        # inference and ranking
        ratings = self.hybrid_model.predict(user_feat, animes_features, user_param, animes_idx, weights=(0.65, 0.35))

        animes_canditate, ratings = self.space.rank(animes_canditate, ratings, desc=True, limit=30)
        ratings = np.clip(ratings, 0.0, 1.0) # clipping the rating to avoid outlier

        return animes_canditate, ratings

        # 237695603822
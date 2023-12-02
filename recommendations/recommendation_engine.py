from recommendations.cluster_module.vector_space import Vector_Space
from DeepLearningNumpy.network import network

class Engine:
    def __init__(self) -> None:
        self.item_model = network()
        self.item_model.load_model("recommendations/saved/numpy_models/content_item_model.pkl")

        self.space = Vector_Space(self.item_model)

    def similar(self, ids:list, blacklist:list):
        return self.space.find_close(ids, blacklist)
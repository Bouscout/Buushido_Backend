# using the last watched show, we return a list of ids of show we want to recommend
from contenu.recommender_system.serieParams import SeriesFetcher
from contenu.recommender_system.userParams import UserParamsManager

class Recommender:
    def __init__(self) -> None:
        self.user_manager = UserParamsManager()
        self.series_fetcher = SeriesFetcher()

    def recommend_shows(self, ids:list) -> list :
        """
        Takes a list a recently watched shows ids and return an ids of recommended shows ids
        """
        u_cluster, user_param = self.user_manager.find_user_cluster(ids)
        u_top_3 = self.user_manager.find_cluster_top_3(u_cluster)

        recommendations = self.series_fetcher.picks(u_top_3, user_param, ids)

        return recommendations
    
    def recommnend_popular(self):
        """
        Send a pick of shows selected from the most popular cluster
        """
        picks = self.series_fetcher.picks_from_popular()
        return picks


from contenu.models import video, cluster
from identifier.models import user_cluster
import numpy as np

class SeriesFetcher:
    def __init__(self, num_recommendations=15) -> None:
        self.num_recommendations = num_recommendations
        
        self.distribution = [45, 35, 20]

    def retrieve_series(self, video_cluster):
        clust = cluster.objects.get(id=video_cluster)
        videos = clust.all_videos()
        return videos
    
    def picks(self, top_3):
        """
        Pick the recommendations according to a distribution based on their cluster rankings
        """
        recommendations = []
        def picks_from_rank(part_size, videos):
            num = self.num_recommendations * part_size
            num = num // 100 
            num = num or 1
            return np .random.choice(videos, size=num)
        
        for index, cluster in enumerate(top_3) :
            videos = self.retrieve_series(cluster)
            size = self.distribution[index]

            for values in picks_from_rank(size, videos) :
                recommendations.append(values)

        return recommendations



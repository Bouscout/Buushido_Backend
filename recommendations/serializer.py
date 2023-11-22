from rest_framework import serializers
from recommendations.models import anime

class Anime_Serializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        slug_field="genre",
        many=True,
        read_only=True
    )
    class Meta :
        model = anime
        fields = ("title", "description", "nsfw", "portrait_pic", "completed", "studios", "num_episodes", "genres", "anime_id", "buushido_id", "start_date", "rating")

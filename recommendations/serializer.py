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
        fields = ("id", "title", "description", "nsfw", "portrait_pic", "completed", "studios", "num_episodes", "genres", "anime_id", "buushido_id", "start_date", "rating")


# for search querying
class Anime_Search_Serializer(serializers.ModelSerializer) :
    genres = serializers.SlugRelatedField(
        slug_field="genre",
        many=True,
        read_only=True
    )

    class Meta :
        model = anime
        fields = ("id", "title", "genres", "portrait_pic")
    
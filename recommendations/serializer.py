from rest_framework import serializers
from recommendations.models import anime

class Anime_Serializer(serializers.ModelSerializer):
    genres = serializers.SlugRelatedField(
        slug_field="genre",
        many=True,
        read_only=True
    )

    classification = serializers.SlugRelatedField(
        slug_field="rating",
        many=True,
        read_only=True
    )

    class Meta :
        model = anime
        fields = ("id", "buushido_id", "title", "english_title", "other_name", "description", "classification", "portrait_pic", "completed", "studios", "producers", "num_episodes", "genres", "anime_id", "rating")


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
    
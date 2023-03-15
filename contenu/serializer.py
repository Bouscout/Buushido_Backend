from rest_framework import serializers
from contenu.models import video, la_video
from gerant.models import onglet, affichage


#serializer for the shows on the home page
class video_serial(serializers.ModelSerializer):
    class Meta:
        model = video   
        fields = ('name', 'background_tof', 'id')

#serializer for the show in categories page
class categorie_serial(serializers.ModelSerializer):
    class Meta :
        model = video
        fields = ('name', 'tof_url', 'id')

#optional
class onglet_serial(serializers.ModelSerializer):
    class Meta:
        model = onglet
        field = []

#serializer for the poster on the home page, but we will probably keep that part static on the build part with astro
class posterialiseur(serializers.ModelSerializer):
    class Meta:
        model = video
        fields = ('name', 'lesstext', 'poster_tof', 'id', )

#serializer for the episodes of a show
class episode_serializer(serializers.ModelSerializer):
    class Meta :
        model = la_video
        fields = ('episode', 'saison', 'url', 'ref')

#serializer for the different attributes of a show
class detail_serie_serializer(serializers.ModelSerializer):
    class Meta :
        model = video
        fields = ('id','name', 'description', 'genre_1', 'genre_2', 'genre_3', 'genre_4', 'tof_url', 'background_tof', 'note', 'date', 'en_cours')

#serializer for the see all page
class voir_tout_serial(serializers.ModelSerializer):
    class Meta:
        model = video
        fields = ('id','name','note', 'en_cours' ,'lesstext', 'genre_1', 'genre_2', 'genre_3','genre_4')

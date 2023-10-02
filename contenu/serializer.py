from rest_framework import serializers
from contenu.models import video, la_video, films
from gerant.models import onglet, affichage

class video_serial(serializers.ModelSerializer):
    class Meta:
        model = video   
        fields = ('name', 'background_tof', 'id', 'tof_url', 'note', "lesstext", "genre_1", "genre_2", "genre_3","genre_4", "en_cours")

class onglet_special(serializers.ModelSerializer):
    class Meta :
        model = video
        fields = ('name', 'background_tof' ,'background_tof2', 'id', 'note')

class categorie_serial(serializers.ModelSerializer):
    class Meta :
        model = video
        fields = ('name', 'tof_url', 'background_tof', 'id')

class onglet_serial(serializers.ModelSerializer):
    class Meta:
        model = onglet
        field = []

class posterialiseur(serializers.ModelSerializer):
    class Meta:
        model = video
        fields = ('name', 'lesstext', 'poster_tof', 'tof_url', 'id', 'genre_1', 'genre_2', 'genre_3')

class episode_serializer(serializers.ModelSerializer):
    class Meta :
        model = la_video
        fields = ('episode', 'saison', 'url', 'url2', 'url3', 'special')

class episode_info(serializers.ModelSerializer):
    serie = video_serial(source="nom", read_only=True)
    # photo = serializers.SlugRelatedField(queryset="nom",read_only=True ,slug_field="tof_url")

    class Meta :
        model = la_video
        fields = ("nom", "episode", "saison", "date", "serie")

class film_serializer(serializers.ModelSerializer):
    class Meta :
        model = films
        fields = ('saison', 'url', 'url2', 'url3', 'special_name')

class detail_serie_serializer(serializers.ModelSerializer):
    class Meta :
        model = video
        fields = ('id','name', 'description', 'genre_1', 'genre_2', 'genre_3', 'genre_4', 'tof_url', 'background_tof', 'note', 'date', 'en_cours', 'saisons', 'has_film', 'couleur')


class voir_tout_serial(serializers.ModelSerializer):
    class Meta:
        model = video
        fields = ('id','name','note', 'en_cours' ,'lesstext', 'genre_1', 'genre_2', 'genre_3','genre_4')




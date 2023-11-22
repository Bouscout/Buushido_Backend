from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# models for the recommendations app
# everything will explicitly be written in english in order to facilitate the consuption of api bu other parties
app_name = "recommendations"

# all possibles genres
class genres(models.Model):
    genre = models.CharField(max_length=100)
    class Meta :
        app_label = "recommendations"
    
    def __str__(self) -> str:
        return str(self.genre)

# different seperations of anime
class cluster(models.Model):
    centroid = models.BinaryField(default=None, null=True)
    class Meta :
        app_label = "recommendations"
    def __str__(self) -> str:
        return f"cluster : {self.id}"


class anime(models.Model) :
    # basic informations
    title = models.CharField(max_length=150)
    description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=True) # if all the episodes have aired
    studios = models.CharField(max_length=150, null=True, blank=True)
    num_episodes = models.IntegerField(default=12)

    genres = models.ManyToManyField(genres, default=None)
    
    # link to corresponding show in buushido, a foreigh key would be correct, but I don't want to create dependancy with the
    # "contenu" app
    buushido_id = models.IntegerField(null=True, default=None) 
    anime_id = models.IntegerField(null=True, default=None)

    # visual information
    portrait_pic = models.URLField(default=None, null=True)

    # informations for filters
    nsfw = models.BooleanField(default=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, default=None)
    
    rating = models.DecimalField(
        default=5.0,
        max_digits=4,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ]
    )

    # vector and ML information
    features_vector = models.BinaryField(default=None, null=True) # numpy vector of shape(84,)
    params_vector = models.BinaryField(default=None, null=True) # numpy vector of shape(256,)
    cluster = models.ForeignKey(cluster, on_delete=models.SET_NULL, null=True)

    class Meta :
        app_label = "recommendations"

    def __str__(self) -> str:
        return str(self.title)

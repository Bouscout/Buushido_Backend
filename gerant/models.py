from django.db import models
from contenu.models import video


class onglet(models.Model):
    name = models.CharField(max_length=60, blank=True, null=True)
    description_onglet = models.TextField(verbose_name='Small description for the content of the onglet'
                                   ,blank=True,
                                    null=True)
    onglet1 = models.ManyToManyField(video, blank=True)
    order_id = models.PositiveSmallIntegerField(default=0)
    links_choix = (
        ('Action' , 'Action'),
        ('Aventure', 'Aventure'),
        ('Comedie', 'Comedie'),
        ('Drama', 'Drama'), 
        ('Horreur', 'Horreur'),
        ('Romance', 'Romance'),
        ('Sci-fi', 'Sci-fi'),
        ('Slice of life', 'Slice of life'),
        ('Mystere', 'Mystere'),
        ('Seinen', 'Seinen'),
        ('Isekai', 'Isekai'),
        ('Shonen', 'Shonen'),
        ('Sport', 'Sport'),
        ('Fantaisie', 'Fantaisie'),
        ('Shojo', 'Shojo'),
        ('Thriller', 'Thriller'),
        ('Combat', 'Combat'),
        ('School life', 'School life'),
        ('Music', 'Music'),
        ('Ecchi', 'Ecchi'),
        ('Autres', 'Autres'),
        ('Classique', 'Classique'),
        ('Film', 'Film'),
    )
    link_to = models.CharField('conduit vers : ', max_length = 50, choices= links_choix, blank=True, null=True)

    def __str__(self):
        return self.name
# Create your models here.

    

class affichage(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    poster = models.ManyToManyField(video, blank=True, verbose_name='Les posters a afficher')
    to_display = models.ManyToManyField(onglet, blank=True)

    def __str__(self) :
        return self.name

class calendrier(models.Model):
    nom = models.CharField(max_length=10)
    # upgrade = models.FileField(upload_to='')
    Dimanche = models.CharField(max_length=50, default='N/A')
    Lundi = models.CharField(max_length=50, default='N/A')
    Mardi = models.CharField(max_length=50, default='N/A')
    Mercredi = models.CharField(max_length=50, default='N/A')
    Jeudi = models.CharField(max_length=50, default='N/A')
    Vendredi = models.CharField(max_length=50, default='N/A')
    Samedi = models.CharField(max_length=50, default='N/A')

    def __str__(self):
        return self.nom

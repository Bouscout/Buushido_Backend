from django.db import models
from contenu.models import video


#these classes are for the different section in the main page of the website

class onglet(models.Model):
    name = models.CharField(max_length=60, blank=True, null=True)
    onglet1 = models.ManyToManyField(video, blank=True)
    order_id = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.name
# Create your models here.

    

class affichage(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    poster = models.ManyToManyField(video, blank=True, verbose_name='Les posters a afficher')
    to_display = models.ManyToManyField(onglet, blank=True)

    def __str__(self) :
        return self.name


#class created for the implementation of a potential calendar function
class calendrier(models.Model):
    nom = models.CharField(max_length=10)

    Dimanche = models.CharField(max_length=50, default='N/A')
    Lundi = models.CharField(max_length=50, default='N/A')
    Mardi = models.CharField(max_length=50, default='N/A')
    Mercredi = models.CharField(max_length=50, default='N/A')
    Jeudi = models.CharField(max_length=50, default='N/A')
    Vendredi = models.CharField(max_length=50, default='N/A')
    Samedi = models.CharField(max_length=50, default='N/A')

    def __str__(self):
        return self.nom



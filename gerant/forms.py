from gerant.models import onglet
from django import forms
from contenu.models import video, la_video
from django import forms

#all the forms for the CRUD operations on the database

#optional form
class onglet_form(forms.ModelForm) :
    class Meta:
        model = onglet
        fields = ['name']

#form to define a new section in the home page
class onglet_serie(forms.ModelForm):
    editeur = forms.NullBooleanField(widget=forms.HiddenInput, initial=True)
    class Meta:
        model = onglet
        fields = ('name','description_onglet','link_to','onglet1')
        widgets = {
        'onglet1': forms.CheckboxSelectMultiple()
        }
        labels = {
            'name': 'Nom de l\'onglet' ,
            'onglet1':'choisissez en minimum sept(7) et maximum 14' ,
        }

#form to display all the shows by order in the home page of the gerant page
class onglet_serie2(forms.Form):
    name = forms.CharField(label='Nom ou Description de l\'onglet')
    editeur = forms.NullBooleanField(widget=forms.HiddenInput, initial=True)
    choix = [] + [(int(x.id), x) for x in video.objects.all().order_by('name')]
    onglet1 = forms.MultipleChoiceField(choices=choix,
    widget=forms.CheckboxSelectMultiple() ,
    )
    
#form to delete a section
class supprimer_onglet(forms.Form):
    supprimer= forms.NullBooleanField(widget=forms.HiddenInput, initial=True)

#form to delete an episode of a show
class supprimer_episode(forms.Form):
    supprimer= forms.NullBooleanField(widget=forms.HiddenInput, initial=True)
    
#form to select the poster to display on the main page       
class affichage_form(forms.Form):
    choix = [('rien', 'Ne rien changer ici')] + [(int(x.id), x) for x in video.objects.all().order_by('name')]
    choix2 = [('rien', 'Ne rien changer ici')] + [(int(x.id), x) for x in onglet.objects.all() ]
    poster = forms.MultipleChoiceField(choices=choix,
    widget=forms.CheckboxSelectMultiple() ,
    label= 'Choisissez les posters a afficher'
    )
    to_display = forms.MultipleChoiceField(choices=choix2, 
        widget=forms.CheckboxSelectMultiple() ,
        label='Onglet a afficher'
    )
   
#form to create or edit a show attributes
class formulaire_video(forms.ModelForm):
    couleur = forms.CharField(label='Couleur d\'ambiance', max_length=7,
    widget=forms.TextInput(attrs={'type': 'color'}))
    class Meta:
        model = video
        fields= ['name', 'other_name', 'posteur', 'genre_1', 'genre_2', 'genre_3','genre_4','couleur','note', 'en_cours', 'tof_url', 'background_tof', 'background_tof2','poster_tof' ,'description', 'lesstext', 'saisons', 'has_film' ]

#form to enter the create an episode to a show
class formulaire_episode(forms.ModelForm):
    class Meta:
        model = la_video
        fields = ['episode', 'url', 'url2', 'url3', 'special']
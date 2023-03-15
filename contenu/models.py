
from cProfile import label
from email.policy import default
from django.db import models
from django.conf import settings
from colorfield.fields import ColorField
from PIL import Image


#this class is for the tv shows and all the underlying informations concerning them

class video(models.Model):
    name = models.CharField('nom', max_length=100)
    tof_url = models.ImageField(upload_to='media/' , blank=True, null = True)
    background_tof = models.ImageField(upload_to='media/', blank=True, null=True)
    poster_tof = models.ImageField(upload_to='media/', blank=True, null=True)
    posteur = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,default=None, on_delete=models.SET_DEFAULT)
    description = models.TextField(null=True, blank=True)
    lesstext = models.TextField(blank=True, null=True)
    moretext = models.TextField(blank=True, null=True)
    couleur = ColorField(default='#f9f5f5')
    order_id = models.PositiveSmallIntegerField(default=0)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    note = models.FloatField(default=8.0)
    en_cours = models.BooleanField(default=False)
    genre_choix = (
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
        ('Film', 'Film'),
    )
    genre_1 = models.CharField('genre', max_length = 50, choices= genre_choix, )
    genre_2 = models.CharField('genre', max_length = 50, choices= genre_choix, blank = True, null= True)
    genre_3 = models.CharField('genre', max_length = 50, choices= genre_choix, blank = True, null= True)
    genre_4 = models.CharField('genre', max_length = 50, choices= genre_choix, blank = True, null= True)
    genres = models.CharField(max_length = 200, blank = True, null = True)  

 

    def __str__(self):
        return str(self.name)

    #In order to reduce the size of the pics and change them to next gen format
    def pic(self):
        photo1 = Image.open(self.tof_url)
        photo2 = Image.open(self.background_tof)
        photo1 = photo1.resize((480, 720))
        photo2 = photo2.resize((1280, 720))
        photo1.save(self.tof_url.path+'.webp', format="webp", optimize=True, quality = 60, subsampling=0)
        photo2.save(self.background_tof.path+'.webp', format="webp", optimize=True, quality=60, subsampling=0)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.pic()

    #this will set specific table in the database allowing to quickly analyze all the genres of a show without having to individually pull
    # all the genre table
    def naming(self):
        self.genres = str(f'{self.genre_1} {self.genre_2} {self.genre_3} {self.genre_4}')

    
    #this function check for the description of a given show and then make a short version of it for more pratical use cases
    def text(self):
        # if len(str(self.lesstext)) > 50 :
        #     return
        tr = str(self.description)
        mid = 0
        x = 200
        try:
            while True:
                if tr[x] == '.':
                    mid = x
                    break
                x += 1
        except IndexError:
            return
        self.lesstext = tr[0:mid+1]
        self.moretext = tr[mid+1:]

    #return all the shows at a given index
    def search_value(self, index):
        return video.objects.filter(name__startswith = index)

    #not relevant anymore, used to allow the usage of google drive hosted image
    def framing_links(self):
        first = str(self.tof_url)
        second = str(self.background_tof)
        self.tof_url = 'https://drive.google.com/uc?export=view&id=' + first[32:65]
        self.background_tof = 'https://drive.google.com/uc?export=view&id=' + second[32:65]
        if self.poster_tof:
            third = str(self.poster_tof)
            self.poster_tof = 'https://drive.google.com/uc?export=view&id=' + third[32:65]
    


#this class is for storing all the episodes and relate them to the concerning show
class la_video(models.Model):
    episode = models.PositiveIntegerField(verbose_name='===> Ecrivez le chiffre correspondant a l\'episode')
    saison = models.PositiveIntegerField('la saison correspondant a l\'episode',blank=True, null = True, default=1)
    nom = models.ForeignKey(video, on_delete=models.CASCADE, null=True)
    url = models.CharField(max_length = 200, blank=True, null = True)
    url2 = models.CharField(max_length = 200, blank=True, null = True)
    ref = models.PositiveIntegerField(null=True, blank=True)
    special = models.CharField(max_length=30, default=None, null=True, blank=True)

    def __str__(self):
        return str(self.nom) + 'S' + str(self.saison) + ' episode ' + str(self.episode)

    #function used in the first version of the site to allow the user to dynamically change episode
    def get_ref(self):
        self.ref = int(str(self.saison)+str(self.episode))

    
    #function to get the src of a link from the different hosting websites
    def fullscreen(self):
        obj = str(self.url)
        obj = obj.lower()
        a=0
        b=0
        for i in range(len(obj[5:])) :
            if obj[i-3] != 's':
                continue
            if obj[i-3] + obj[i-2] + obj[i-1] + obj[i] == 'src=' :
                a = i + 2
                break
        for x in range(a+10, len(obj[5:])):
            if obj[x] == ' ' :
                b = x-1
                break
        if b > a :
            self.url = obj[a:b]
        if self.url2 :
            obj = str(self.url2)
            obj = obj.lower()
            a=0
            b=0
            for i in range(len(obj[5:])) :
                if obj[i-3] != 's':
                    continue
                if obj[i-3] + obj[i-2] + obj[i-1] + obj[i] == 'src=' :
                    a = i + 2
                    break
            for x in range(a+10, len(obj[5:])):
                if obj[x] == ' ' :
                    b = x-1
                    break
            if b > a :
                self.url2 = obj[a:b]


        
        

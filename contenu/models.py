
from django.db import models
from django.conf import settings
from colorfield.fields import ColorField
from PIL import Image


class video(models.Model):
    # the different names of the show
    name = models.CharField('nom', max_length=100)
    other_name = models.CharField(max_length=100, blank=True, null=True)

    # the different pictures representing the show
    tof_url = models.ImageField(upload_to='portrait/' , blank=True, null = True)
    background_tof = models.ImageField(upload_to='paysage/', blank=True, null=True)
    background_tof2 = models.ImageField(upload_to='paysage_2/', blank=True, null=True)
    poster_tof = models.ImageField(upload_to='poster/', blank=True, null=True)

    # user that posted the show
    posteur = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,default=None, on_delete=models.SET_DEFAULT)

    # description texts and styling
    description = models.TextField(null=True, blank=True)
    lesstext = models.TextField(blank=True, null=True)
    couleur = ColorField(default='#f9f5f5')
    order_id = models.PositiveSmallIntegerField(default=14)
    note = models.FloatField(default=8.0)
    en_cours = models.BooleanField(default=False)

    date = models.DateField(auto_now_add=True, null=True, blank=True)
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
        ('Classique', 'Classique'),
        ('Film', 'Film'),
    )
    genre_1 = models.CharField('genre', max_length = 50, choices= genre_choix, )
    genre_2 = models.CharField('genre', max_length = 50, choices= genre_choix, blank = True, null= True)
    genre_3 = models.CharField('genre', max_length = 50, choices= genre_choix, blank = True, null= True)
    genre_4 = models.CharField('genre', max_length = 50, choices= genre_choix, blank = True, null= True)
    genres = models.CharField(max_length = 200, blank = True, null = True)  

    # string to contain informations about the saison names
    saisons = models.TextField(blank=True, null=True)
    has_film = models.BooleanField(default=False)

    # ML informations
    cluster = models.ForeignKey("cluster", on_delete=models.SET_NULL, null=True)

    # numpy arrays
    feature_array = models.BinaryField(default=None, null=True)
    params_array = models.BinaryField(default=None, null=True)

    def __str__(self):
        return str(self.name)

    #In order to reduce the size of the pics and change them to next gen format
    def pic(self, reso2=(768, 480), reso=(240, 384)):
        # we'// check if they are in the new location otherwise they must be at the old one
        try :
            photo1 = Image.open(self.tof_url)
        except FileNotFoundError :
            tof_url = '/home/buushido/buushido/media/media/' + self.tof_url.path.split('/')[-1]
            photo1 = Image.open(tof_url)

        # same process for the backgground tof
        try :
            photo2 = Image.open(self.background_tof)
        except FileNotFoundError :
            back_url = '/home/buushido/buushido/media/media/' + self.background_tof.path.split('/')[-1]
            photo2 = Image.open(back_url)


        photo1 = photo1.resize(reso)
        photo2 = photo2.resize(reso2)
        try :
            photo3 = Image.open(self.background_tof2)
            photo3 = photo3.resize(reso2)

            # we are going to edit the code below in order to serve the files in production
            # photo3.save(self.background_tof2.path+'.webp', format='webp', optimize=True, quality=80, subsampling=0)
            path_b3 = '/home/buushido/buushido/public/media/paysage_2/' + self.background_tof2.path.split('/')[-1] 

            photo3.save(path_b3 +'.webp', format='webp', optimize=True, quality=80, subsampling=0)
        except : 
            pass
        path_portrait = '/home/buushido/buushido/public/media/portrait/' + self.tof_url.path.split('/')[-1] 
        path_paysage = '/home/buushido/buushido/public/media/paysage/' + self.background_tof.path.split('/')[-1] 

        photo1.save(path_portrait +'.webp', format="webp", optimize=True, quality = 80, subsampling=0)
        photo2.save(path_paysage  +'.webp', format="webp", optimize=True, quality=80, subsampling=0)

        # photo1.save('/public/portrait'+ self.tof_url.path +'.webp', format="webp", optimize=True, quality = 80, subsampling=0)
        # photo2.save('/public/paysage' + self.background_tof.path +'.webp', format="webp", optimize=True, quality=80, subsampling=0)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # self.pic()

    # in order to find the querry the genre of a show without having to pull all 4 genres classes when searching
    def naming(self):
        self.genres = str(f'{self.genre_1} {self.genre_2} {self.genre_3} {self.genre_4}')

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


    def search_value(self, index):
        return video.objects.filter(name__startswith = index)

    def framing_links(self):
        first = str(self.tof_url)
        second = str(self.background_tof)
        self.tof_url = 'https://drive.google.com/uc?export=view&id=' + first[32:65]
        self.background_tof = 'https://drive.google.com/uc?export=view&id=' + second[32:65]
        if self.poster_tof:
            third = str(self.poster_tof)
            self.poster_tof = 'https://drive.google.com/uc?export=view&id=' + third[32:65]
    
    #method to affect whole database
    @classmethod
    def lost(cls):
        pass


#model for handling the division of the video model in to different clusters for embedding purposes
class cluster(models.Model):
    centroid = models.BinaryField(default=None, null=True)
    def __str__(self) -> str:
        return f"cluster : {self.pk}"
    
    def all_videos(self) :
        return self.video_set.all()
    
class special_cluster(models.Model) :
    name = models.CharField(max_length=100)
    videos = models.ManyToManyField("video", default=None)

    def __str__(self) -> str:
        return f"special cluster : {self.name}"
    
    def all_videos(self):
        return self.videos.all()




# it would be too complicated to declare a film inside la_video class without having to loop to find it
# instead we are going to make a specific table for the film and tie it with the video object
class films(models.Model) :
    name = models.ForeignKey(video, on_delete=models.CASCADE, null=True)
    special_name = models.CharField(max_length=100) # the name to add to the show name
    saison = models.PositiveIntegerField(default=0) # the saison it comes right after if inside a show
    url = models.CharField(max_length = 200, blank=True, null = True)
    url2 = models.CharField(max_length = 200, blank=True, null = True)
    url3 = models.CharField(max_length = 200, blank=True, null = True)
    
    



class la_video(models.Model):
    episode = models.PositiveIntegerField(verbose_name='===> Ecrivez le chiffre correspondant a l\'episode')
    saison = models.PositiveIntegerField('la saison correspondant a l\'episode',blank=True, null = True, default=1)
    nom = models.ForeignKey(video, on_delete=models.CASCADE, null=True)

    # url infos
    url = models.CharField(max_length = 200, blank=True, null = True)
    url2 = models.CharField(max_length = 200, blank=True, null = True)
    url3 = models.CharField(max_length = 200, blank=True, null = True)
    direct_url = models.CharField(max_length=200, blank=True, null=True)

    # extra
    ref = models.PositiveIntegerField(null=True, blank=True)
    special = models.CharField(max_length=30, default=None, null=True, blank=True)

    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.nom) + 'S' + str(self.saison) + ' episode ' + str(self.episode)

    def get_ref(self):
        self.ref = int(str(self.saison)+str(self.episode))

    # parsing the correct link
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


        
        
# Create your models here.

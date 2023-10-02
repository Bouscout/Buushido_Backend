from django.db import models

# Create your models here.

class WebTraffic(models.Model):

    # using charfield for num of views just in case it gets too big
    num_views_inTimeframe = models.IntegerField(default=1)

    date = models.DateTimeField(auto_now_add=True)

    user_info = models.TextField(default=' ')

    class Meta : 
        app_label = 'metrics'

    def __str__(self):
        return str(f"{self.date} : {self.num_views_inTimeframe}")

# num of user being connected for a only a brief moment
# we are going to find the num of user who are here for not a brief moment
# then find the ratio with total num of user

class Not_brief_connection(models.Model):

    num_user_staying = models.IntegerField(default=1)

    date = models.DateTimeField(auto_now_add=True)

    class Meta :
        app_label = 'metrics'

    def __str__(self):
        return str(f"{self.date} : {self.num_user_staying}")
    
# when uou migrate use the extra_db
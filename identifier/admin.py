from django.contrib import admin
from contenu.models import video, la_video
from identifier.models import utilisateur
from gerant.models import onglet, affichage, calendrier

class video_admin(admin.ModelAdmin):
    pass
admin.site.register(video, video_admin)
admin.site.register(utilisateur, video_admin)
admin.site.register(la_video, video_admin)
admin.site.register(onglet, video_admin)
admin.site.register(affichage, video_admin)
admin.site.register(calendrier, video_admin)

from typing import Any
from django.contrib import admin
from django.contrib.admin import AdminSite, sites
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from contenu.models import video, la_video
from identifier.models import utilisateur
from gerant.models import onglet, affichage, calendrier
from metrics import models as metrics_model
from django.contrib import admin
from django.db.models.base import ModelBase
from django.apps import apps

# from django.db.migrations.recorder import MigrationRecorder
# from django.db.migrations.recorder import MigrationRecorder
# [(m.app, m.name) for m in MigrationRecorder.Migration.objects.all()]

class my_anime_admin(admin.ModelAdmin):
    using = "my_anime_db"
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).using(self.using)
    
class metrics_admin(admin.ModelAdmin):
    using = "extra_db"
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).using(self.using)


# Register models from the 'recommendations' app
apps_model = apps.get_app_config("recommendations").get_models()
for model in apps_model:
    admin.site.register(model, my_anime_admin)


apps_model = apps.get_app_config("contenu").get_models()
for model in apps_model :
    admin.site.register(model)

apps_model = apps.get_app_config("metrics").get_models()
for model in apps_model :
    admin.site.register(model, metrics_admin)


apps_model = apps.get_app_config("identifier").get_models()
for model in apps_model :
    admin.site.register(model)

apps_model = apps.get_app_config("gerant").get_models()
for model in apps_model :
    admin.site.register(model)

# apps_model = apps.get_app_config("recommendations").get_models()
# for model in apps_model :
#     admin.site.register(model)


# Very hacky!
# for name, var in metrics_model.__dict__.items():
#     if type(var) is ModelBase:
#         admin.site.register(var)

# class video_admin(admin.ModelAdmin):
#     pass
# admin.site.register(video, video_admin)
# admin.site.register(utilisateur, video_admin)
# admin.site.register(la_video, video_admin)
# admin.site.register(onglet, video_admin)
# admin.site.register(affichage, video_admin)
# admin.site.register(calendrier, video_admin)
# admin.site.register(MigrationRecorder.Migration, video_admin)

"""anime URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from identifier.views import maintenance
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
# from rest_framework.authtoken import views

# all apps urls

urlpatterns = [
    path('', include('contenu.contenu_urls')),
    path('gerant/', include('gerant.gerant_urls')),
    path('', include('identifier.iden_urls')),
    path('metrics/', include('metrics.urls_metrics')),
    path("recommendations/", include("recommendations.recommender_urls")),
    path("admin/", admin.site.urls),
    # path('api/token/', views.obtain_auth_token, name='token_obtain_pair'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]  
if settings.DEBUG :
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

handler404 = "anime.views.maintenance"

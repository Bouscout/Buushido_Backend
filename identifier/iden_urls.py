from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.home_login, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('choix/<choix>', views.add_watchlist, name='watchlist'),
    path('test/', views.test, name='test'),
]
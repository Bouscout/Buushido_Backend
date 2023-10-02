from django.urls import path
from . import views, serial_view_iden
urlpatterns = [
    path('loginold/', views.home_login, name='login'),
    path('signup/', views.sign_up, name='signup'),
    path('choix/<choix>', views.add_watchlist, name='watchlist'),
    # path('test/', views.maintenance, name='test'),
    # path('test2/', views.test3, name='test3'),

    path('api/signup/', serial_view_iden.create_user.as_view(), name='api_signup'),
    path('api/test_log/', serial_view_iden.view_test.as_view(), name='api_log'),
]
from django.urls import path, include
from django.conf import settings
from app import views as app_views
from django.conf.urls.static import static



urlpatterns = [
        path('',app_views.home, name='home'),
        path('create/',app_views.create, name='create'),
        path('vote/<id>/',app_views.vote, name='home'),
        path('results/<id>/',app_views.results, name='results'),
        path('accounts/register/', app_views.register, name ='register'),
        path('accounts/login/', app_views.login, name ='login'),
         
]

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app import views as app_views

from django.contrib.auth import views as auth

urlpatterns = [
    # path('',include('app.urls')),
    path('', app_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('create/', app_views.create, name='create'),
    path('vote/<poll_id>/', app_views.vote, name='vote'),
    path('results/<poll_id>/', app_views.results, name='results'),
    path('delete/<poll_id>/', app_views.delete, name='delete'),

    path('details/', app_views.profile, name ='details'),
    path('login/', app_views.Login, name ='login'),
    path('logout/', app_views.Logout, name ='logout'),
    path('register/', app_views.register, name ='register'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

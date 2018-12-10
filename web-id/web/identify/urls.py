from . import views
from django.urls import path
from django.conf.urls import url, include

urlpatterns = [
    path('', views.index, name='index'),
    path('register',views.register, name='register'),
    path('login', views.login, name='login')
]

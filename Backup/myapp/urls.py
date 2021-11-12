from os import name
from typing import Counter
from django.urls import path
from . import views
from django.conf.urls import url
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('bookmark/<str:usr>', views.bookmark, name='bookmark'),
    path('detail/<int:deid>', views.detail, name='detail'),
    path('upload', views.upload, name='upload'),
    path('profile/<str:usr>', views.userprofile, name='profile'),
    path('profile/setting/<str:uss>', views.profilesetting, name='profilesetting'),
    path('account/setting/<str:uss>', views.account, name='account'),
    path('personal/<str:uss>', views.personal, name='personal'),
    path('update/<int:iid>', views.update, name='update'),
    path('ads/<str:usr>', views.userads, name='userads'),
    path('delete/<item_pk>', views.delete, name='delete-item'),
    path('dashboard/<str:usr>', views.dashboard, name='dashboard')
]
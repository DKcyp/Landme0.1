from django.contrib.auth.models import User
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save
from string import Template
from django.utils.safestring import mark_safe
class item(models.Model):
    title = models.CharField(max_length=100)
    detail = models.CharField(max_length=255)
    display = models.BooleanField(default=True)
    images = models.ImageField(upload_to='images/', null=True)
    userid = models.ForeignKey(User, on_delete=CASCADE)
    harga = models.IntegerField()
    luas = models.IntegerField()
    lokasi = models.CharField(max_length=100)
    keunikan = models.CharField(max_length=100, null=True, blank=True)
    aksesair = models.CharField(max_length=100, null=True, blank=True)
    sertifikasi = models.CharField(max_length=100, null=True, blank=True)
    datecreated = models.DateTimeField(auto_now_add=True)
    dateupdated = models.DateTimeField(auto_now=True)
    
    def geturl(self):
        return reverse("detail", kwargs={"deid": self.id})

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    userpic = models.ImageField(upload_to='profile/',null=True,blank=True, default='default.png')
    bio = models.CharField(max_length=255, null=True, blank=True)
    fullname = models.CharField(max_length=255, null=True,blank=True)
    headline = models.CharField(max_length=255, null=True,blank=True)
    products = models.ManyToManyField(item)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
	    if created:
		    Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
	    instance.profile.save()

class personaldata(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    phonenum = models.CharField(max_length=15,null=True,blank=True)
    nowa = models.CharField(max_length=15,null=True,blank=True)
    address = models.CharField(max_length=255, null=True,blank=True)
    pob = models.CharField(max_length=255, null=True,blank=True)
    dob = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=255, null=True,blank=True)
    @receiver(post_save, sender=User)
    def create_user_personaldata(sender, instance, created, **kwargs):
	    if created:
		    personaldata.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_personaldata(sender, instance, **kwargs):
	    instance.personaldata.save()
#     # def geturlx(self):
#     # def geturlx(self):
#     # def geturlx(self):
#     #     return reverse("profilesetting", kwargs={"uss": self.username})

        
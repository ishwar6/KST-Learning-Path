from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
import random
import os
from userstates.models import UserState
User = get_user_model()

def upload_image_path_profile(instance, filename):
    new_filename = random.randint(1,9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "profile/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
    )
         

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


ROLE_CHOICES = (
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
        (11, '11'),
        (12, '12'),
    )

class Profile(models.Model):
    user         =   models.OneToOneField(User, on_delete= models.CASCADE)
    name         =   models.CharField(max_length=120,  blank = True, null = True)
    email        =   models.EmailField( blank = True, null = True)
    image = models.ImageField(upload_to = upload_image_path_profile, default=None, null = True, blank = True)
    standard     =   models.IntegerField(choices=ROLE_CHOICES, default=10)
    city         =   models.CharField(max_length = 30, blank = True, null = True)
    count        =   models.IntegerField(default=0)


    def __str__(self):
        return str(self.user) + '  ' + str(self.name)


        

def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user = instance)
post_save.connect(user_created_receiver, sender = User)




def user_created_receiver_for_userstates(sender, instance, created, *args, **kwargs):
    if created:
        UserState.objects.get_or_create(user = instance)
post_save.connect(user_created_receiver_for_userstates, sender = User)



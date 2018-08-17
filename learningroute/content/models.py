from django.db import models
from states.models import State
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save,post_save
from django.core.validators import MinValueValidator , MaxValueValidator



def upload_image_path_content(instance, filename):
    new_filename = random.randint(1,9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "content/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )

def upload_image_path_illus(instance, filename):
    new_filename = random.randint(1,9996666666)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "illustrations/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


class Content(models.Model):
    state   =   models.ForeignKey(State, on_delete=models.CASCADE)
    title   =   models.CharField(max_length=120, blank=False, null=False)
    text    =   models.TextField()
    image   =   models.FileField(upload_to = upload_image_path_content, null = True, blank = True)
    image2  =   models.FileField(upload_to = upload_image_path_content, null = True, blank = True)
    credit  =   models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default='1', blank=False)
    time    =   models.IntegerField()
    tag     =   models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return  str(self.title) + ' -- for the state -- ' + str(self.state)

    #def get_absolute_url(self):
    #    return reverse('content:detail', kwargs={"slug": self.state})


class Illustration(models.Model):
    content   =   models.ForeignKey(Content, on_delete=models.CASCADE)
    title     =   models.CharField(max_length=120, blank=False, null=False)
    text      =   models.TextField()
    answer    =   models.TextField()
    image     =   models.FileField(upload_to = upload_image_path_illus, null = True, blank = True)
    image2    =   models.FileField(upload_to = upload_image_path_illus, null = True, blank = True)
    credit    =   models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default='3', blank=False)
    time      =   models.IntegerField()


    def __str__(self):
        return  str(self.title)

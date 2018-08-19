from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save,post_save
from django.core.validators import MinValueValidator , MaxValueValidator
from django.utils.text import slugify

import random
import os
import string


CHAPTER_CHOICE = (
('algebra', 'Algebra'),
('calculus', 'Calculas'),
('geometry', 'Geometry'),
('trigo', 'Trigonometry'),
('cartgeo', 'Cartesian-Geometry'),
('others', 'Others')
)


def unique_slug_generator(instance, new_slug =None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    if slug in Dont_use:
       new_slug = "{slug} - {randstr}".format(
       slug = slug,
       randstr = random_string_generator(size=4)
        )
       return unique_slug_generator(instance, new_slug= new_slug)

    klass = instance.__class__
    qs_exists = klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug} - {randstr}".format(
        slug = slug,
        randstr = random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug= new_slug)
    return slug



def random_string_generator(size=5, chars = string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def upload_image_path_chapters(instance, filename):
    new_filename = random.randint(1,910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "chapters/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )

def upload_image_path_topics(instance, filename):
    new_filename = random.randint(1,999910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "topics/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )

def upload_image_path_questions(instance, filename):
    new_filename = random.randint(1,9910209312)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "questions/{new_filename}/{final_filename}".format(
            new_filename=new_filename,
            final_filename=final_filename
            )



def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext



class Chapter(models.Model):
    title = models.CharField(max_length = 80, blank = False,)
    gaurd = models.CharField(max_length = 120, default = 'others', choices = CHAPTER_CHOICE)
    standard = models.IntegerField( default = '10', blank = False)
    slug = models.SlugField(blank = True, null = True)
    image = models.FileField(upload_to = upload_image_path_chapters, null = True, blank = True)




    class Meta:
        db_table = 'Chapter'
    def __str__(self):
       return self.title
    # def get_absolute_url(self):
    #
    #     return reverse('chapters:detail', kwargs={"slug": self.slug})


def rl_pre_save_receiver(sender,instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender= Chapter)



class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title = models.CharField(max_length = 80, blank = False)
    content1 = models.TextField(max_length = 30000, blank = False)
    image1 = models.FileField(upload_to = upload_image_path_topics, null = True, blank = True)
    content2 = models.TextField(max_length = 30000, blank = True)
    image2 = models.FileField(upload_to = upload_image_path_topics, null = True, blank = True)
    slug = models.SlugField(blank = True, null = True)


    class Meta:
        db_table = 'Topic'
    def __str__(self):
       return self.title



def topic_pre_save_receiver(sender,instance, *args, **kwargs):
        if not instance.slug:
            instance.slug = unique_slug_generator(instance)

pre_save.connect(topic_pre_save_receiver, sender= Topic)




class Question(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    question = models.TextField(max_length = 40000, blank = False)
    qimage = models.FileField(upload_to = upload_image_path_questions, null = True, blank = True)
    answer = models.TextField(max_length = 40000, blank = True)
    aimage = models.FileField(upload_to = upload_image_path_questions, null = True, blank = True)



    def __str__(self):
       return self.question

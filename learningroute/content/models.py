from django.db import models
from states.models import State
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save,post_save
from django.core.validators import MinValueValidator , MaxValueValidator
from chapters.models import Chapter
from django.contrib.auth import get_user_model

User = get_user_model()

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
    state   =   models.OneToOneField(State, on_delete=models.CASCADE)
    title   =   models.CharField(max_length=120, blank=False, null=False)
    text    =   models.TextField()
    image   =   models.FileField(upload_to = upload_image_path_content, null = True, blank = True)
    image2  =   models.FileField(upload_to = upload_image_path_content, null = True, blank = True)
    credit  =   models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default='2', blank=False,  help_text= 'Give a number according to difficulty of content between 1 to 5')
    time    =   models.IntegerField(default='6', help_text='Time in minutes')
    tag     =   models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return  str(self.title) + ' -- for the state -- ' + str(self.state)

    #def get_absolute_url(self):
    #    return reverse('content:detail', kwargs={"slug": self.state})

class IllusManager(models.Manager):
    def topic_count(self, topic):
        count_ = 0
        states  = State.objects.filter(topic = topic)
        for state in states:
            content = Content.objects.filter(state = state).first()
            if content:
                illus_count = self.filter(content = content).last().counts
                if illus_count:
                    return illus_count
        return count_
            


class Illustration(models.Model):
    content   =   models.ForeignKey(Content, on_delete=models.CASCADE)
    text      =   models.TextField(blank = False, null = False )
    answer    =   models.TextField(blank = True, null = True)
    image     =   models.FileField(upload_to = upload_image_path_illus, null = True, blank = True)
    image2    =   models.FileField(upload_to = upload_image_path_illus, null = True, blank = True)
    credit    =   models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)], default='2', blank=False, help_text= 'Give a number according to difficulty of illustration between 1 to 5')
    time      =   models.IntegerField(default='3', help_text='Time in minutes')
    counts    =   models.IntegerField(blank = True, null = True, help_text='Leave it blank')

    objects   = IllusManager()


    def __str__(self):
        return  str(self.text)


def illus_created_reciever(sender, instance, *args, **kwargs):
            illust_last  =  Illustration.objects.filter(content = instance.content)
            if illust_last.exists():
                illust_last_count = illust_last.last().counts
                instance.counts   = illust_last_count + 1
            else:
                instance.counts = 1

        
pre_save.connect(illus_created_reciever, sender=Illustration)


################################################
# User specific models #

class IllusManager(models.Manager):
    def user_topic_count(self, topic):
        user = self.request.user
        count_ = 0
        states  = State.objects.filter(topic = topic)
        for state in states:
            content = Content.objects.filter(state = state).first()
            if content:
                illus_count = self.filter(content = content, user = user).first().counts
                if illus_count:
                    count_ = count_ + illus_count
        return count_


    def user_chapter_count(self, chapter):
        user = self.request.user
        count_ = 0
        topics  = Topic.objects.filter(chapter = chapter)
        for topic in topics:
            topic_count = topic.user_topic_count(self, topic)
            if topic_count:
                count_ = count_ + topic_count
        return count_


class IllustrationGiven(models.Model):
    user         = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    content      = models.ForeignKey(Content, on_delete = models.CASCADE)
    count        = models.IntegerField(default=0, help_text='Will increase as the student will solve illustrations')
    timestamp    = models.DateTimeField(auto_now_add = True)

    objects      = IllusManager()

    def __str__(self):
        return str(self.user) + ' has solved ' + str(self.count)


# will keep all active chapters of student with complete boolean 0 or 1. @@ get_or_create will be used here to access. 
class CurrentActiveChapter(models.Model):
    user         = models.ForeignKey(User, on_delete= models.CASCADE)
    chapter      = models.ForeignKey(Chapter, on_delete= models.CASCADE)
    done         = models.BooleanField(default = 0)
    timestamp    = models.DateTimeField(auto_now_add= True)
    timeupdate   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user) + ' is in ' + str(self.chapter) + ' with status ' + str(self.done)



# this model keep track of student's activity on a particular state. 
# Amount of illustrations solved, and amount of questions solved on a particular state.

class CurrentActiveState(models.Model):
    user         = models.ForeignKey(User, on_delete= models.CASCADE)
    state        = models.ForeignKey(State, on_delete= models.CASCADE)
    theory       = models.BooleanField(default = 0)
    score_of_i   = models.IntegerField(default=0, help_text='Will increase as the student will solve illustrations')
    score_of_q   = models.IntegerField(default=0, help_text='Will increase as the student will solve Questions')
    timestamp    = models.DateTimeField(auto_now_add= True)
    timeupdate   = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.state) + ' is active for ' + str(self.user)


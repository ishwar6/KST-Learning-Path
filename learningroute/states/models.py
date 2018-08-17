from django.db import models



class State(models.Model):
    title = models.CharField(max_length = 120, blank = False, null = False)
    topic = models.CharField(max_length = 222)
    rate = models.IntegerField()
    time = models.IntegerField()
    tag  = models.CharField( max_length = 15, blank = True, null = True  )


    def __str__(self):
        return self.title + ' - for the topic - ' + self.topic







from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class UserState(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE,default=None)
    state       = models.ForeignKey(State, on_delete= models.CASCADE, default = None)
    correct_q   = models.IntegerField(default = 0)
    stage       = models.IntegerField(default = 0)
    time_taken  = models.IntegerField(blank = True, null = True)
    timedate    = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return str(self.user) + ' - ' + str(self.stage)

    

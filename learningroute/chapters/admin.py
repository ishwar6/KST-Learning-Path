from django.contrib import admin

from .models import Chapter, Topic, Question
from django.db import models



class TopicAdmin(admin.ModelAdmin):

  search_fields = ['chapter','title'  ]
  list_display = ('title', 'chapter')
  list_filter = ('chapter',)

class QuestionAdmin(admin.ModelAdmin):

  search_fields = ['question','topic'  ]
  list_display = ('question','topic', )
  list_filter = ('topic',)

admin.site.register(Chapter)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)

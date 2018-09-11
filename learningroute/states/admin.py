# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import State, Node, Edge
from django.db.models.functions import Lower
from chapters.models import Topic, Chapter 

class NodeInline(admin.TabularInline):
    model = Node.state_node.through

class StateAdmin(admin.ModelAdmin):
    def chapters(self, obj):
        topic  = obj.topic.title
        chapter = Topic.objects.filter(title = topic).first().chapter
        return chapter

    def get_ordering(self, request):
        return [Lower('topic_id')]  # sort case insensitive



    list_display = ('title', 'topic', 'pk', 'tag', 'chapters')
    inlines = [
        NodeInline,
    ]   

    


class NodeAdmin(admin.ModelAdmin):

    inlines = [
        NodeInline,
    ]
    exclude = ('state_node',)

admin.site.register(Node, NodeAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(Edge)

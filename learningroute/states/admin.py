# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import State, Node, Edge



class NodeInline(admin.TabularInline):
    model = Node.state_node.through

class StateAdmin(admin.ModelAdmin):
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

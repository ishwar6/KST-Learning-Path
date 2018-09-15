# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import  TempActiveNode, UserCurrentNode
# Register your models here.

admin.site.register(TempActiveNode)
admin.site.register(UserCurrentNode)

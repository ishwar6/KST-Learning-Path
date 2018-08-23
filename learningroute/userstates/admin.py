# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Proficiency, TempActiveNode, UserCurrentNode
# Register your models here.
admin.site.register(Proficiency)
admin.site.register(TempActiveNode)
admin.site.register(UserCurrentNode)

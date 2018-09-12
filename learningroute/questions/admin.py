# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from questions.models import *

admin.site.register(Question)

admin.site.register(QuestionResponse)
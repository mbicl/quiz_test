from django.contrib import admin
from .models import TestGroup, Test

admin.site.register(Test)
admin.site.register(TestGroup)

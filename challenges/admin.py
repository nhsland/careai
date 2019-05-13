from django.contrib import admin
from .models import Challenge


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('title','get_developers')
# Register your models here.


admin.site.register(Challenge, ChallengeAdmin)

from django.contrib import admin
from .models import Solution



class SolutionAdmin(admin.ModelAdmin):
    list_display = ('title','developer')
# Register your models here.

# Register your models here.
admin.site.register(Solution, SolutionAdmin)

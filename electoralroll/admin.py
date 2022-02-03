from django.contrib import admin

# Register your models here.


from .models import *

admin.site.register(City)
admin.site.register(LegislativeAssembly)
admin.site.register(Voter)
admin.site.register(PartNumber)
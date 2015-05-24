from django.contrib import admin

# Register your models here

from models import principalDB, usrDB, seleccionDB

admin.site.register(principalDB) 
admin.site.register(usrDB) 
admin.site.register(seleccionDB)
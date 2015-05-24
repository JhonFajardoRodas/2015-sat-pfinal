from django.db import models

# Create your models here.




class principalDB(models.Model):
    titulo = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    precio = models.CharField(max_length=32)
    hora = models.DateTimeField()
    duracion = models.DateField()
    url = models.URLField()
    tipo = models.CharField(max_length=100)



class seleccionDB(models.Model):
    idUser = models.IntegerField()
    idEvento = models.IntegerField()
    horaAdd = models.DateTimeField()


class usrDB (models.Model):
    nombre = models.CharField(max_length=100)
    tituloPag  = models.CharField(max_length=100)
    descripcion = models.TextField(null=True)
    color = models.TextField(null=True)
    size = models.TextField(null=True)
    

    
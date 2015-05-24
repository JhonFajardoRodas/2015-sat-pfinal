from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from bs4 import BeautifulSoup
import urllib
from models import principalDB, usrDB, seleccionDB
import time
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template.loader import get_template
from django.template import Context
# Create your views here.


horaActual = time.strftime("%H:%M:%S") #Formato de 24 horas
fechaActual = time.strftime("%d/%m/%y")
def login_user(request):

    
    if request.user.is_authenticated():
        usuario = request.user.username
        try: 
            yes = usrDB.objects.get(nombre=usuario)
        
            respuestaLogin =  ("Bienvenid@: " + request.user.username)
        except:
            entrada= usrDB(nombre=usuario, tituloPag="Pagina de "+ usuario)   
            entrada.save()
            respuestaLogin =  ("Bienvenid@: " + request.user.username)
        return respuestaLogin
    else:
    
        respuestaLogin =  ("Registro")
        
        return respuestaLogin

def principal(request):

    lineas = principalDB.objects.all()
    num_eventos = len(lineas)
    if(num_eventos==0):
        fich = urllib.urlopen("http://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&"+
                                "format=xml&file=0&filename=206974-0-agenda-eventos-culturales-100&mgmtid=6c0b6d01df986410VgnVCM2000000c205a0aRCRD");

        allXml = BeautifulSoup(fich, "xml")
        eventos = allXml.findAll('contenido')
        num_eventos = len(eventos)
        titulos = []
        fechas = []
        precios = []
        urls = []
        horas = []
        duracion = []
        tipo = []
        
        line = 0
        while line < num_eventos:
            titulos = eventos[line].find(nombre='TITULO').string
            fechasX = eventos[line].find(nombre='FECHA-EVENTO').string.split(" ")[0]
            try:
                urls = eventos[line].find(nombre='CONTENT-URL').string
            except:
                urls = "Link does not exist"
            horasX = eventos[line].find(nombre='HORA-EVENTO').string
            fechas = fechasX+ " " + horasX + ":00+00:00"
            horas = fechasX+ " " + horasX  + ":00+00:00"
            duracion = eventos[line].find(nombre='FECHA-FIN-EVENTO').string.split(" ")[0]
            
            try:
                tipo = eventos[line].find(nombre='TIPO').string
            except:
                tipo = "evento"
            try:
                precios = eventos[line].find_all(nombre='PRECIO').string
            except:
                precios = "Consultar en Mas informacion"
            
            entrada = principalDB(titulo=titulos, fecha=fechas, precio=precios, hora=horas, duracion=duracion, url= urls, tipo=tipo)

            entrada.save()
            line = line + 1

    allEventosProx = principalDB.objects.order_by("fecha")[:10]
    allUsers = usrDB.objects.all()
    print allUsers
    allId = seleccionDB.objects.all()
    arrayUsers = []
    arrayEventos = []
    usersEventos = [] # array de los eventos de cada idUsuario
    selEventos = []
    for us in range(len(allId)):
        users = usrDB.objects.get(id=allId[us].idUser)
        selEventos = seleccionDB.objects.filter(idUser=allId[us].idUser)
        usersEventos.append(selEventos)
        arrayUsers.append(users.nombre)

  
    
    for linea in selEventos:
        evento = principalDB.objects.get(id=linea.idEvento)
        arrayEventos.append(evento.titulo)
        
     
    i = 0  
    lista = []
    for i in range(len(selEventos)):
        lista.append(selEventos[i].idEvento)
    

    
    userTitulo = []
    x = 0
    for x  in range(len(lista)):
        tag = principalDB.objects.get(id=lista[x])
        userTitulo.append(tag.titulo)

    
    usuario = request.user.username
    dentro = request.user.is_authenticated()
    plantilla = get_template('plantilla.html')
    plantilla2 = get_template('prueba.html')
    c = Context({'allEventosProx':allEventosProx, 'logueo': login_user(request),
                 'usuarios': allUsers, 'usuario':usuario, 'dentro':dentro})
    p = Context({'lista':usersEventos})
    plantillaHtml = plantilla.render(c)
    plantillaHtml2 = plantilla2.render(p)
    
    
    return HttpResponse(plantillaHtml)



def infoActividad(request, recurso):
    dentro = request.user.is_authenticated()
    usuario = request.user.username
    total = principalDB.objects.all()
    evento = recurso
    urls =  principalDB.objects.filter(url='Link does not exist')
    entrada = principalDB.objects.get(id=evento)
    plantilla = get_template('plantillaEvento.html')
    c = Context({'evento':entrada, 'dentro':dentro, 'usuario': usuario})
    return HttpResponse(plantilla.render(c))


def todas (request):

    dentro = request.user.is_authenticated()
    print dentro
    total = principalDB.objects.all()
    usuario = request.user.username
    
    num_eventos = str(len(total))
    plantilla = get_template('plantillaTodas.html')
    c = Context({'total':total, 'num_eventos': num_eventos, 'logueo': login_user(request),
     'fechaActual': fechaActual, 'horaActual':horaActual, 'dentro':dentro, 'usuario':usuario})
    plantillaTodas = plantilla.render(c)
    if request.method == 'POST':
        filtro= request.body.split("=")[1]
        try:
            respuesta = principalDB.objects.order_by(filtro)

            plantilla = get_template('plantillaTodas.html')
            c = Context({'total':respuesta})
            plantillaTodas = plantilla.render(c)
            return HttpResponse(plantillaTodas)
        except:
            plantilla = get_template('plantillaTodas.html')
            c = Context({'fallo': 'Campo invalido de filtrado'})
            plantillaTodas = plantilla.render(c)
            return HttpResponse(plantillaTodas)
    return HttpResponse(plantillaTodas)


def loguear(request):
    formHtml = "<html><body><h1> <u>Registro:</u>" 
    formHtml += '<form action="" method="POST">'
    formHtml += '<h4>Usuario: <input type= "text" name="valor"</h4>'
    formHtml += '<h4>Password: <input type= "password" name="password"</h4>'
    formHtml += '<input type="submit">'
    formHtml += '</form>'
    formHtml +=  "</h1></body></html>"
    salida = " "
    if request.method == 'POST':
        salida = request.body
        usuario = salida.split("valor=")[1].split("&")[0]

        password = salida.split("password=")[1]
        
        user = authenticate(username=usuario, password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect("/")
        else:

            return HttpResponseRedirect("/")

    return HttpResponse(formHtml)


def expulsar(request):
    logout(request)
    return HttpResponseRedirect("/")




def actualizar(request):
    
    
    total = principalDB.objects.all()
    fich = urllib.urlopen("http://datos.madrid.es/portal/site/egob/menuitem.ac61933d6ee3c31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a0aRCRD&"+
                            "format=xml&file=0&filename=206974-0-agenda-eventos-culturales-100&mgmtid=6c0b6d01df986410VgnVCM2000000c205a0aRCRD");

    allXml = BeautifulSoup(fich, "xml")
    eventos = allXml.findAll('contenido')
    num_eventos = len(eventos)
    titulos = []
    fechas = []
    precios = []
    urls = []
    horas = []
    duracion = []
    tipo = []
    
    line = 0
    while line < num_eventos:
        titulos = eventos[line].find(nombre='TITULO').string

        fechasX = eventos[line].find(nombre='FECHA-EVENTO').string.split(" ")[0]
        try:
            urls = eventos[line].find(nombre='CONTENT-URL').string
        except:
            urls = "Link does not exist"
        horasX = eventos[line].find(nombre='HORA-EVENTO').string
        fechas = fechasX+ " " + horasX + ":00+00:00"
        horas = fechasX+ " " + horasX  + ":00+00:00"
        duracion = eventos[line].find(nombre='FECHA-FIN-EVENTO').string.split(" ")[0]
        
        try:
            tipo = eventos[line].find(nombre='TIPO').string
        except:
            tipo = "evento"
        try:
            precios = eventos[line].find_all(nombre='PRECIO').string
        except:
            precios = "Consultar en Mas informacion"
        
        igual = False
        for current in total:
            if current.titulo == titulos:
                if str(current.fecha) == fechas:
                    print ">>>>>>>>>>> Aqui Entro  2 <<<<<<<<<<<"
                    igual = True

        if (igual == False):
            entrada = principalDB(titulo=titulos, fecha=fechas, precio=precios, hora=horas, duracion=duracion, url= urls, tipo=tipo)
            entrada.save()
        
        line = line + 1
    global horaActual
    horaActual = time.strftime("%H:%M:%S") #Formato de 24 horas
    global fechaActual
    fechaActual = time.strftime("%d/%m/%y")

    
    
    return HttpResponseRedirect("/todas")


def seleccionar (request, recurso):
    print str(request.body)
    idRecurso = recurso
    usuario = request.user.username
    idUser = usrDB.objects.get(nombre=usuario)
    eventos = seleccionDB.objects.filter(idUser=idUser.id)
    esta = False
    for linea in eventos:
        if(str(linea.idEvento) == str(idRecurso)):
            print "Aqui entro"
            esta = True
    if(esta==False):
        entrada = seleccionDB(idUser=idUser.id, idEvento=idRecurso, horaAdd=datetime.datetime.now())
        entrada.save()

    return  HttpResponseRedirect("/todas")

def pagUsuario (request, recurso):
    dentro = False
    otro = False
    print dentro
    usuario = request.user.username
     
    filaUsuario = usrDB.objects.get(nombre=recurso)
    if request.user.username == filaUsuario.nombre:
        dentro = True
    else:
        if request.user.is_authenticated():
            otro = True
    idEventos = seleccionDB.objects.filter(idUser=filaUsuario.id)
    
    arrayEventos = []

    for linea in idEventos:
        arrayEventos.append(principalDB.objects.get(id=linea.idEvento))
        
     
    plantilla2 = get_template('prueba.html')
    p = Context({'lista':filaUsuario, 'eventos': arrayEventos, 'dentro': dentro, 'otro': otro, 'horas': idEventos,
                    'usuario':usuario})
    plantillaHtml2 = plantilla2.render(p)
    return HttpResponse(plantillaHtml2)


def ayuda (request):
    dentro = request.user.is_authenticated()
    usuario = request.user.username
    plantilla = get_template('plantillaAyuda.html')
    p = Context({'Titulo':"Pagina de Ayuda", 'usuario':usuario, 'dentro':dentro})
    plantillaHtml = plantilla.render(p)
    return HttpResponse(plantillaHtml)

def cambioTitulo(request):
    usuario = request.user.username
    if request.method == 'POST':
        usuario = request.user.username
        tipo = request.body.split("=")[0]
        if tipo == 'title':
            newTitulo = request.body.split("=")[1]
            newTitulo = newTitulo.split("+")
            salida=""
            for line in newTitulo:
                salida += line + " "
            linea = usrDB.objects.get(nombre=usuario)
            linea.tituloPag = salida
            linea.save()
        elif tipo == 'description':
            newDescrp = request.body.split("=")[1]
            newDescrp = newDescrp.split("+")
            salida=""
            for line in newDescrp:
                salida += line + " "
            linea = usrDB.objects.get(nombre=usuario)
            linea.descripcion = salida
            linea.save()

        elif tipo == 'color':
            color = request.body.split("=")[1]
            linea = usrDB.objects.get(nombre=usuario)
            linea.color = color
            linea.save()

        elif tipo == 'letra':
            tipoLetra = request.body.split("=")[1]
            linea = usrDB.objects.get(nombre=usuario)
            linea.size = tipoLetra
            linea.save()

        

    return HttpResponseRedirect(usuario)

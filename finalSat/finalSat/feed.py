from django.contrib.syndication.views import Feed
from EventosMadrid.models import usrDB , principalDB, seleccionDB


class feed(Feed):

	title="Mis eventos"
	link="http:localhost:1234"
	description="Mi seleccion de eventos"

	def get_object(self, request, usuario):
		user = usrDB.objects.get(nombre=usuario)
		return seleccionDB.objects.filter(idUser=user.id)

	def items(self, obj):
		eventos = []
		for linea in obj:
			eventos.append(principalDB.objects.get(id=linea.idEvento))
		return eventos


	def item_title(self,item):
		return item.titulo


	def item_link(self,item):
		return 'http://localhost:1234/actividades/' + str(item.id)

	




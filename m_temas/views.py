# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import *
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.contrib.auth.models import User, Group
from m_temas.models import *
from m_generales.models import Bitacora, BitacoraBusqUser
import os
from django.conf import settings 
from django.contrib import messages
from django.db.models import Q
import datetime as dt
from savio.utiles import *
from django.db import connection

def force_to_unicode(text):
	return text if isinstance(text, unicode) else text.decode('latin-1')

def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	]

def floatcomma(value):
	orig = force_unicode(value)
	intpart, dec = orig.split(".")
	intpart = intcomma(intpart) 
	return ".".join([intpart, dec])

# MODULO DE TEMAS
@login_required()
def temas_listado(request):
	listado = list(TmsTema.objects.values(
			'tema_id',
			'tema_nombre',
			'tema_descripcion',
			'tema_estado'
		).all().order_by('-tema_estado', 'tema_nombre'))
	ctx = {
		'listado':listado,
	}
	return render(request, 'temas_listado.html', ctx)

@login_required()
@transaction.atomic
def temas_nuevo(request):
	if request.POST:
		with transaction.atomic():
			try:
				print (request.FILES.get('tema_logo'))
				tema = TmsTema()
				tema.tema_nombre = request.POST['tema_nombre']
				tema.tema_estado = True
				tema.tema_logo = request.FILES.get('tema_logo')
				tema.tema_descripcion = request.POST['tema_descripcion']
				tema.user_creador = request.user
				tema.user_modificador = request.user
				tema.save()
				messages.success(request, 'Tema creado con éxito')
			except Exception as e:
				print (e)
				messages.error(request, 'Ocurrio un problema al crear tema')
				return render(request, 'temas_nuevo.html', {})
		return redirect('temas_listado')
	else:
		ctx={}
		return render(request, 'temas_nuevo.html', ctx)

@login_required()
@transaction.atomic
def temas_editar(request, id):
	if request.POST:
		with transaction.atomic():
			try:
				tema = TmsTema.objects.get(pk = request.POST['id'])
				tema.tema_nombre = request.POST['tema_nombre']
				tema.tema_estado = request.POST['tema_estado']
				tema.tema_descripcion = request.POST['tema_descripcion']
				tema.user_modificador = request.user
				if not request.FILES.get('tema_logo') == None:
					try:
						tema.tema_logo = request.FILES.get('tema_logo')
					except Exception as e:
						print (e)
						messages.warning(request, 'Ocurrio un problema al cambiar logo')
				tema.save()
				messages.success(request, 'Tema editado con éxito')
			except Exception as e:
				print (e)
				messages.error(request, 'Ocurrio un problema al editar tema')
				try:
					tema = TmsTema.objects.get(pk = id)
				except Exception as e:
					print (e)
					messages.warning(request, 'No se pudo obtener tema')
					return redirect('temas_listado')
				ctx={
					'tema':tema
				}
				return render(request, 'temas_editar.html', ctx)
			return redirect('temas_listado')
	else:
		try:
			tema = TmsTema.objects.get(pk = id)
		except Exception as e:
			print (e)
			messages.warning(request, 'No se pudo obtener tema')
			return redirect('temas_listado')
		ctx={
			'tema':tema
		}
		return render(request, 'temas_editar.html', ctx)

@login_required()
def temas_detalle(request, id):
	if request.is_ajax():
		import json
		codigo = request.GET['codigo']
		listado = list(TmsReporte.objects.values('reporte_id','reporte_nombre',
			'reporte_descripcion','reporte_logo').filter(subtema = codigo, reporte_estado = True))
		data = json.dumps({
			'listado':listado,
		})
		return HttpResponse(data, content_type='application/json')
	
	tema = TmsTema.objects.get(pk = id)
	listado_subtemas =list(TmsSubtema.objects.values().filter(tema = id, subtema_estado = True))
	ctx={
		'tema':tema,
		'listado_subtemas':listado_subtemas,		
	}
	return render(request, 'temas_detalle.html', ctx)
# FINAL DE MODULO DE TEMAS 


@login_required()
def busqueda_reporte(request):
	if request.GET:
		data = request.GET['data']
		if data == "Novedades":
			BitacoraBusqUser.objects.create(busq_query=data[:50], user=request.user)
			sub = list(TmsReporte.objects.values_list(
				"subtema", flat=True).order_by("-fecha_creacion")[:10])
			listado_subtemas = list(TmsSubtema.objects.values().filter(
				subtema_id__in=sub, subtema_estado=True))
		elif data == "top":
			BitacoraBusqUser.objects.create(busq_query=data[:50], user=request.user)

			try:
				cursor = connection.cursor()
				query = "SELECT sum(bi.bit_counter) total, rp.subtema_id FROM [dbo].[bitacora] bi "
				query += "INNER JOIN [dbo].[tms_reporte] rp on rp.reporte_id = bi.reporte_id "
				query += "GROUP BY bi.bit_counter, rp.subtema_id ORDER BY total DESC"
				cursor.execute(query)
				result = dictfetchall(cursor)
			except Exception as e:
				print(e)
			finally:
				cursor.close()
			sub = list()
			for x in list(result):
				sub.append(x["subtema_id"])
			listado_subtemas = list(TmsSubtema.objects.values().filter(
				subtema_id__in=sub, subtema_estado=True)[:5])
		else:
			BitacoraBusqUser.objects.create(busq_query=data[:50], user=request.user)
			listado_subtemas = list(TmsSubtema.objects.values().filter(
				subtema_tags__contains=data, subtema_estado=True))
		ctx = {
			'listado_subtemas': listado_subtemas,
			'data': data
		}
		return render(request, 'busqueda_reporte.html', ctx)

# MODULO DE SUBTEMAS
@login_required()
def subtemas_listado(request):
	listado = list( TmsSubtema.objects.values('subtema_id', 'subtema_nombre', 'tema__tema_nombre', 'subtema_estado').all().order_by('-subtema_estado', 'tema__tema_nombre'))
	ctx ={
		'listado':listado
	}
	return render(request, 'subtemas_listado.html', ctx)

@login_required()
@transaction.atomic
def subtemas_nuevo(request):
	if request.POST:
		with transaction.atomic():
			try:
				subtema = TmsSubtema()
				subtema.subtema_nombre = request.POST['subtema_nombre'][:50]
				subtema.subtema_estado = True
				subtema.tema = TmsTema.objects.get(pk = request.POST['tema'])
				subtema.subtema_subnombre = request.POST['subtema_subnombre'][:50] 
				subtema.subtema_descripcion = request.POST['subtema_descripcion'][:500]
				subtema.user_creador = request.user
				subtema.user_modificador = request.user
				subtema.save()
				messages.success(request, 'Subtema creado con éxito')
			except Exception as e:
				print (e)
				messages.error(request, 'Ocurrio un problema al crear subtema')
				listado = list(TmsTema.objects.values('tema_nombre', 'tema_id').all())
				ctx={
					'listado':listado,
				}
				return render(request, 'subtemas_nuevo.html', ctx)
		return redirect('subtemas_listado')
	else:
		listado = list(TmsTema.objects.values('tema_nombre', 'tema_id').all())
		ctx={
			'listado':listado,
		}
		return render(request, 'subtemas_nuevo.html', ctx)

@login_required()
@transaction.atomic
def subtemas_editar(request, id):
	if request.POST:
		with transaction.atomic():
			try:
				subtema = TmsSubtema.objects.get(pk = request.POST['id'])
				subtema.subtema_nombre = request.POST['subtema_nombre'] [:50]
				subtema.subtema_subnombre = request.POST['subtema_subnombre'][:50] 
				subtema.subtema_descripcion = request.POST['subtema_descripcion'][:500]
				subtema.subtema_estado = request.POST['subtema_estado']
				subtema.tema = TmsTema.objects.get(pk = request.POST['tema'])
				subtema.user_modificador = request.user
				subtema.save()
				messages.success(request, 'Subtema editado con éxito')
			except Exception as e:
				print (e)
				messages.error(request, 'Ocurrio un problema al crear subtema')
				try:
					sub = TmsSubtema.objects.get(pk = id)
				except Exception as e:
					print (e)
					messages.warning(request, 'No se pudo obtener sub tema')
					return redirect('subtemas_listado')

				listado = list(TmsTema.objects.values('tema_nombre', 'tema_id').all())
				ctx={
					'listado':listado,
					'sub':sub
				}
				return render(request, 'subtemas_editar.html', ctx)

		return redirect('subtemas_listado')
	else:
		try:
			sub = TmsSubtema.objects.get(pk = id)
		except Exception as e:
			print (e)
			messages.warning(request, 'No se pudo obtener sub tema')
			return redirect('subtemas_listado')

		listado = list(TmsTema.objects.values('tema_nombre', 'tema_id').all())
		ctx={
			'listado':listado,
			'sub':sub
		}
		return render(request, 'subtemas_editar.html', ctx)

@login_required()
@transaction.atomic
def subtemas_detalle(request, id):

	if request.is_ajax():
		import json
		
		data = json.dumps({
			})
		return HttpResponse(data, content_type='application/json')
	elif request.GET:
		pass
	else:
		try:
			sub = TmsSubtema.objects.get(pk = id)
			tags = sub.subtema_tags
			tags = tags.split('#')
			TmsNotificaciones.objects.filter(user=request.user.id, subtema = id).update(activa=False)
		except Exception as e:
			print (e)
			messages.warning(request, 'No se pudo obtener sub tema')
			return redirect('reportes')
		
		mas = False
		listado_principal = list(TmsReporte.objects.filter(subtema= sub.pk, reporte_estado =  True).values(
			'reporte_nombre', 'reporte_descripcion', 'reporte_tags', 'reporte_iframe', 'reporte_id',
			'reporte_is_principal', 'reporte_is_secundario', 'reporte_referencias'
		).order_by('-reporte_is_principal', '-reporte_is_secundario'))
		listado_referencias= ""
		for x in listado_principal:
			i = x["reporte_referencias"]
			ultimo = i[-1]
			if ultimo == ';':
				listado_referencias = listado_referencias + i
			else:
				i = i + ';'
				listado_referencias = listado_referencias + i
			if x['reporte_is_principal'] != True and x['reporte_is_secundario'] != True:
				mas= True
		listado_referencias = listado_referencias.split(";")
		listaIdRelacionados = list()
		listado_relacionados = list()
		reporte_descripcion = ""
		for i in tags:
			i = i.replace(" ", "")
			if i:
				a = i.replace("#", "")
				reporte_descripcion = reporte_descripcion + a + ","
				temp = list()
				temp = list(TmsSubtema.objects.exclude(pk= sub.subtema_id).filter(
					subtema_tags__contains= a, subtema_estado = True).values_list('subtema_id', flat= True))
				for z in temp:
					if z not in listaIdRelacionados:
						listaIdRelacionados.append(z)
		listado_relacionados = list(TmsSubtema.objects.filter(subtema_id__in = listaIdRelacionados))
		ctx ={
			'mas':mas,
			'sub': sub,
			'tags':tags,
			'reporte_descripcion':reporte_descripcion,
			'listado_principal': listado_principal,
			'listado_relacionados':listado_relacionados,
			'listado_referencias':listado_referencias
		}
		return render(request, 'subtemas_detalle.html', ctx)

@login_required()
def reporte_favorito(request):
	if request.GET:
		try:
			id = TmsReporte.objects.get(pk = request.GET["code"])
			sub = TmsSubtema.objects.get(pk=id.subtema.subtema_id)
			tags = sub.subtema_tags
			tags = tags.split('#')
		except Exception as e:
			print (e)
			messages.warning(request, 'No se pudo obtener sub tema')
			return redirect('reportes')
		
		mas = False
		listado_principal = list(TmsReporte.objects.filter(subtema= sub.pk, reporte_estado =  True).values(
			'reporte_nombre', 'reporte_descripcion', 'reporte_tags', 'reporte_iframe', 'reporte_id',
			'reporte_is_principal', 'reporte_is_secundario', 'reporte_referencias'
		).order_by('-reporte_is_principal', '-reporte_is_secundario'))
		listado_referencias= ""
		for x in listado_principal:
			i = x["reporte_referencias"]
			ultimo = i[-1]
			if ultimo == ';':
				listado_referencias = listado_referencias + i
			else:
				i = i + ';'
				listado_referencias = listado_referencias + i
			if x['reporte_is_principal'] != True and x['reporte_is_secundario'] != True:
				mas= True
		listado_referencias = listado_referencias.split(";")
		listaIdRelacionados = list()
		listado_relacionados = list()
		reporte_descripcion = ""
		for i in tags:
			i = i.replace(" ", "")
			if i:
				a = i.replace("#", "")
				reporte_descripcion = reporte_descripcion + a + ","
				temp = list()
				temp = list(TmsSubtema.objects.exclude(pk= sub.subtema_id).filter(
					subtema_tags__contains= a, subtema_estado = True).values_list('subtema_id', flat= True))
				for z in temp:
					if z not in listaIdRelacionados:
						listaIdRelacionados.append(z)
		listado_relacionados = list(TmsSubtema.objects.filter(subtema_id__in = listaIdRelacionados))
		ctx ={
			'mas':mas,
			'sub': sub,
			'tags':tags,
			'reporte_descripcion':reporte_descripcion,
			'listado_principal': listado_principal,
			'listado_relacionados':listado_relacionados,
			'listado_referencias':listado_referencias
		}
		return render(request, 'subtemas_detalle.html', ctx)


@login_required()
def reportes_listado(request, subtema):
	if request.is_ajax():
		import datetime as dt
		import json
		codigo = request.GET['codigo']
		try:
			if not Bitacora.objects.filter(reporte = codigo, user = request.user.id).exists():
				Bitacora.objects.create(
					user = request.user,
					reporte = TmsReporte.objects.get(pk = codigo),
					bit_last_date = dt.datetime.today(),
					bit_counter = 1
				)
			else:
				bita = Bitacora.objects.get(reporte = codigo, user = request.user.id)
				bita.bit_last_date = dt.datetime.today()
				bita.bit_counter = bita.bit_counter + 1
				bita.save()
			
		except Exception as e:
			print(e)
		
		try:
			if not BitacoraRptVisitas.objects.filter(reporte = codigo).exists():
				BitacoraRptVisitas.objects.create(
					reporte=TmsReporte.objects.get(pk=codigo),
					acumulador_visitas = 0,
					acumulador_segundos = 0
					)
			#del request.session['lastRptViewed']
			if not 'lastRptViewed' in request.session or not request.session['lastRptViewed']:
				x = dict()
				x['id'] = codigo
				x['momentStar'] = str(dt.datetime.timestamp(dt.datetime.now()))
				request.session['lastRptViewed'] = [x]
			else:
				lastRptViewed = request.session['lastRptViewed'][0]["id"]
				momentStar = request.session['lastRptViewed'][0]["momentStar"]
				momentStar = dt.datetime.fromtimestamp(float(momentStar))
				momentEnd = dt.datetime.now()
				totalSeconds = momentEnd - momentStar
				try:
					rpt = BitacoraRptVisitas.objects.get(reporte=lastRptViewed)
					rpt.acumulador_visitas = rpt.acumulador_visitas +1
					temp = float(rpt.acumulador_segundos) + totalSeconds.total_seconds()
					rpt.acumulador_segundos = "{0:.2f}".format(temp)
					rpt.save()
				except Exception as e:
					print(e)
				x = dict()
				x['id'] = codigo
				x['momentStar'] = str(dt.datetime.timestamp(dt.datetime.now()))

				del request.session['lastRptViewed']
				request.session['lastRptViewed'] = [x]
		except Exception as e:
			print (e)

		listado = TmsReporte.objects.values('reporte_iframe').get(pk = codigo)
		try:
			favorito = TmsFavoritos.objects.values("id").get(reporte=codigo, user=request.user.id)
		except Exception as e:
			print (e)
			favorito = False
		data = json.dumps({
			'listado':listado,
			'favorito': favorito
		})
		return HttpResponse(data, content_type='application/json')

	try:
		sub = TmsSubtema.objects.get(pk = subtema)
	except Exception as e:
		print (e)
		messages.warning(request, 'No se pudo obtener sub tema')
		return redirect('subtemas_listado')
	listado = TmsReporte.objects.values(
		'reporte_id','reporte_nombre','reporte_descripcion',
		'reporte_estado','reporte_gratuito', 'subtema__subtema_nombre'
		).filter(subtema = subtema).order_by('-reporte_estado', 'reporte_nombre')

	ctx = {
		'listado':listado,
		'sub':sub
	}
	return render(request, 'reportes_listado.html', ctx)
 

@login_required()
def doFavorito(request):
	if request.is_ajax():
		import json
		codigo = request.GET['codigo']
		try:
			if not TmsFavoritos.objects.filter(reporte=codigo, user=request.user.id).exists():
				print ("if")
				favo = TmsFavoritos()
				favo.reporte=TmsReporte.objects.get(pk = codigo)
				favo.user = request.user
				favo.save()
				fav = TmsFavoritos.objects.values().get(pk=favo.pk)
			else:
				print("else")
				TmsFavoritos.objects.filter(reporte=codigo, user=request.user.id).delete()
				fav = False
				
		except Exception as e:
			print(e)
		data = json.dumps({
			'favorito': fav,
			'codigo':codigo
		})
		return HttpResponse(data, content_type='application/json')


@login_required()
@transaction.atomic
def reportes_nuevo(request, subtema):
	if request.POST:
		with transaction.atomic():
			try:
				try:
					print (request.POST['reporte_is_principal'] )
					if request.POST['reporte_is_principal'] == '1':
						TmsReporte.objects.filter(subtema= request.POST['subtema']).update(
							reporte_is_principal = 0
						)
				except Exception as e:
					pass

				try:
					print (request.POST['reporte_is_secundario'] )
					if request.POST['reporte_is_secundario'] == '1':
						TmsReporte.objects.filter(subtema= request.POST['subtema']).update(
							reporte_is_secundario = 0
						)
				except Exception as e:
					pass

				rpt = TmsReporte()
				rpt.reporte_nombre = request.POST['reporte_nombre'][:50]
				rpt.reporte_descripcion = request.POST['reporte_descripcion'][:500]
				rpt.reporte_estado = request.POST['reporte_estado']

				rpt.reporte_iframe = request.POST['reporte_iframe'][:5000]
				rpt.reporte_referencias = request.POST['reporte_referencias'][:5000]
				rpt.reporte_tags = request.POST['reporte_tags'][:100]
				
				rpt.reporte_gratuito = request.POST['reporte_gratuito']
				try:
					rpt.reporte_is_principal = request.POST['reporte_is_principal']
				except Exception as e:
					pass 
				
				try:
					rpt.reporte_is_secundario = request.POST['reporte_is_secundario']
				except Exception as e:
					pass
				
				rpt.subtema = TmsSubtema.objects.get(pk = request.POST['subtema'])
				rpt.user_creador = request.user
				rpt.user_modificador = request.user
				rpt.save()
				

				data = list(TmsReporte.objects.filter(subtema= request.POST['subtema']).
					values_list('reporte_tags', flat=True))
				temp= ''
				for x in data:
					temp= temp + ' '+ x
				TmsSubtema.objects.filter(pk = request.POST['subtema'] ).update(
					subtema_tags = temp
				)

				messages.success(request, 'Reporte creado con éxito')
			except Exception as e:
				print (e)
				messages.error(request, 'Ocurrio un problema al crear reporte')

				try:
					sub = TmsSubtema.objects.get(pk = subtema)
				except Exception as e:
					print (e)
					messages.warning(request, 'No se pudo obtener sub tema')
					return redirect('subtemas_listado')
				ctx = {
					'sub':sub
				}
		return redirect(reverse('reportes_listado', kwargs={'subtema': request.POST['subtema']}))
	else:
		try:
			sub = TmsSubtema.objects.get(pk = subtema)
		except Exception as e:
			print (e)
			messages.warning(request, 'No se pudo obtener sub tema')
			return redirect('subtemas_listado')
		ctx = {
			'sub':sub
		}
		return render(request, 'reportes_nuevo.html', ctx)

@login_required()
@transaction.atomic
def reportes_editar(request, id):
	if request.POST:
		with transaction.atomic():
			try:
				try:
					if request.POST['reporte_is_principal'] == '1':
						TmsReporte.objects.filter(subtema= request.POST['subtema']).update(
							reporte_is_principal = 0
						)
				except Exception as e:
					pass

				try:
					if request.POST['reporte_is_secundario'] == '1':
						TmsReporte.objects.filter(subtema= request.POST['subtema']).update(
							reporte_is_secundario = 0
						)
				except Exception as e:
					pass

				rpt = TmsReporte.objects.get(pk = request.POST['id'])
				rpt.reporte_nombre = request.POST['reporte_nombre'][:50]
				rpt.reporte_descripcion = request.POST['reporte_descripcion'][:500]
				rpt.reporte_estado = request.POST['reporte_estado']
				rpt.reporte_iframe = request.POST['reporte_iframe'][:5000]
				rpt.reporte_referencias = request.POST['reporte_referencias'][:5000]
				rpt.reporte_tags = request.POST['reporte_tags'][:100]
				rpt.reporte_gratuito = request.POST['reporte_gratuito']
				try:
					rpt.reporte_is_principal = request.POST['reporte_is_principal']
				except Exception as e:
					if rpt.reporte_is_principal == True:
						rpt.reporte_is_principal = False
				
				try:
					rpt.reporte_is_secundario = request.POST['reporte_is_secundario']
				except Exception as e:
					if rpt.reporte_is_secundario == True:
						rpt.reporte_is_secundario = False
				rpt.user_modificador = request.user
				rpt.save()
				
				data = list(TmsReporte.objects.filter(subtema= request.POST['subtema']).
					values_list('reporte_tags', flat=True))
				temp= ''
				for x in data:
					temp= temp + ' '+ x
				TmsSubtema.objects.filter(pk = request.POST['subtema'] ).update(
					subtema_tags = temp
				)

				messages.success(request, 'Reporte editado con éxito')
			except Exception as e:
				print (e)
				messages.error(request, 'Ocurrio un problema al editar reporte')

				try:
					sub = TmsSubtema.objects.get(pk = subtema)
				except Exception as e:
					print (e)
					messages.warning(request, 'No se pudo obtener sub tema')
					return redirect('subtemas_listado')
				ctx = {
					'sub':sub
				}
		return redirect(reverse('reportes_listado', kwargs={'subtema': request.POST['subtema']}))

		return redirect('subtemas_listado')
	else:
		try:
			rpt = TmsReporte.objects.get(pk = id)
		except Exception as e:
			print (e)
			messages.warning(request, 'No se pudo obtener el reporte')
			return redirect('subtemas_listado')
		ctx={
			'rpt':rpt
		}
		return render(request, 'reportes_editar.html', ctx)

@login_required()
def getNotification(request):
	if request.is_ajax():
		import json
		user = request.user.id
		listado = list(TmsNotificaciones.objects.filter(user = user, activa = True).values(
			'subtema__subtema_id', 'subtema__subtema_nombre',  'fecha_creacion', 'id'))
		data = json.dumps({
			'listado': listado,
		}, default=convert_date_str)
		return HttpResponse(data, content_type='application/json')

@login_required()
def desNotification(request):
	if request.is_ajax():
		codigo = request.GET["codigo"]
		if codigo == 0:
			TmsNotificaciones.objects.filter(user =request.user.id).update(activa = False)
		else:
			TmsNotificaciones.objects.filter(pk = codigo).update(activa = False)
		import json
		user = request.user.id
		listado = list(TmsNotificaciones.objects.filter(user = user, activa = True).values(
			'subtema__subtema_id', 'subtema__subtema_nombre', 'fecha_creacion', 'id'))
		print (listado)
		data = json.dumps({
			'listado': listado,
		}, default=convert_date_str)
		return HttpResponse(data, content_type='application/json')


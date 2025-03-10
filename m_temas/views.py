# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import *
#from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.contrib.auth.models import User, Group
from m_temas.models import *
import os
from django.conf import settings 
from django.contrib import messages

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
				tema = TmsTema()
				tema.tema_nombre = request.POST['tema_nombre']
				tema.tema_estado = True
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
				subtema.subtema_nombre = request.POST['subtema_nombre']
				subtema.subtema_estado = True
				subtema.tema = TmsTema.objects.get(pk = request.POST['tema'])
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
				subtema.subtema_nombre = request.POST['subtema_nombre']
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
def reportes_listado(request, subtema):
	try:
		sub = TmsSubtema.objects.get(pk = subtema)
	except Exception as e:
		print (e)
		messages.warning(request, 'No se pudo obtener sub tema')
		return redirect('subtemas_listado')
	listado = TmsReporte.objects.values(
		'reporte_id','reporte_nombre','reporte_descripcion',
		'reporte_estado','reporte_gratuito',
		).filter(subtema = subtema).order_by('-reporte_estado', 'reporte_nombre')

	ctx = {
		'listado':listado,
		'sub':sub
	}
	return render(request, 'reportes_listado.html', ctx)


@login_required()
@transaction.atomic
def reportes_nuevo(request, subtema):
	if request.POST:
		with transaction.atomic():
			try:
				subtema = TmsSubtema()
				subtema.subtema_nombre = request.POST['subtema_nombre']
				subtema.subtema_estado = True
				subtema.tema = TmsTema.objects.get(pk = request.POST['tema'])
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
		return redirect('reportes_listado')
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
def detalle_tema(request, codigo):
	tema = TmsTema.objects.get(pk = codigo)
	listado_subtemas =list(GralSubtema.objects.values().filter(tema = codigo))
	ctx={
		'tema':tema,
		'listado_subtemas':listado_subtemas,		
	}
	return render(request, 'detalle_tema.html', ctx)

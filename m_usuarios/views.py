# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import *
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, Group, Permission
from m_usuarios.forms import *
import os 
from django.conf import settings
from django.db.models import Count, Sum 
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
#from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.humanize.templatetags.humanize import *
from m_generales.models import (Bitacora, AuthGroupExtended)
from savio.utiles import *
 
@login_required()
@transaction.atomic
def grupos_listado(request):
	listado= Group.objects.all()
	ctx = {
		'listado': listado,
	}
	return render(request, 'grupos_listado.html', ctx )

@login_required()
@transaction.atomic
def grupos_crear(request):
	if request.POST:
		with transaction.atomic():
			try:
				gp = Group()
				gp.name = request.POST['name'][:80]
				gp.save()
				gr = AuthGroupExtended()
				gr.group = gp
				gr.group_status = request.POST['group_status']
				gr.group_for_client = request.POST['group_for_client']
				if request.POST['group_for_client'] == "0":
					gr.group_subtitulo = ""
					gr.group_detalle = ""
					gr.group_sub_detalle = ""
					gr.group_need_price = ""
					gr.group_price_month = 0
					gr.group_price_anual = 0
					gr.group_price_detalle = ""
				else:
					gr.group_subtitulo = request.POST['group_subtitulo'][:50]
					gr.group_detalle = request.POST['group_detalle'][:500]
					gr.group_sub_detalle = request.POST['group_sub_detalle'][:500]
					gr.group_need_price = request.POST['group_need_price']
					if request.POST['group_need_price'] == "1":
						gr.group_price_month = is_number(request.POST['group_price_month'])
						gr.group_price_anual = is_number(request.POST['group_price_anual'])
						gr.group_price_detalle = ""
					else:
						gr.group_price_month = 0
						gr.group_price_anual = 0
						gr.group_price_detalle = request.POST['group_price_detalle'][:20]
				gr.save()
				for x in request.POST.getlist('permisos'):
					per = Permission.objects.get(id = x)
					gp.permissions.add(per)
				messages.success(request, 'Grupo creado con éxito')
			except Exception as e:
				print (e)
				messages.error(request, 'Ocurrió un problema al crear grupo')
		return redirect('grupos_listado')
	else:
		listado_permisos = Permission.objects.all().order_by('-content_type')
		ctx = {
			'listado_permisos':listado_permisos,
		}
		return render(request, 'grupos_crear.html', ctx )

@login_required()
@transaction.atomic
def grupos_editar(request, id):
	if request.POST:
		with transaction.atomic():
			try:
				gp = Group.objects.get(pk = request.POST['id'])
				gp.name = request.POST['name'][:80]
				gp.save()
				gr = AuthGroupExtended.objects.get(pk = gp.pk)
				gr.group_status = request.POST['group_status']
				gr.group_for_client = request.POST['group_for_client']
				if request.POST['group_for_client'] == "0":
					gr.group_subtitulo = ""
					gr.group_detalle = ""
					gr.group_sub_detalle = ""
					gr.group_need_price = ""
					gr.group_price_month = 0
					gr.group_price_anual = 0
					gr.group_price_detalle = ""
				else:
					gr.group_subtitulo = request.POST['group_subtitulo'][:50]
					gr.group_detalle = request.POST['group_detalle'][:500]
					gr.group_sub_detalle = request.POST['group_sub_detalle'][:500]
					gr.group_need_price = request.POST['group_need_price']
					if request.POST['group_need_price'] == "1":
						gr.group_price_month = is_number(request.POST['group_price_month'])
						gr.group_price_anual = is_number(request.POST['group_price_anual'])
						gr.group_price_detalle = ""
					else:
						gr.group_price_month = 0
						gr.group_price_anual = 0
						gr.group_price_detalle = request.POST['group_price_detalle'][:20]
				gr.save()
				gp.permissions.clear()
				for x in request.POST.getlist('permisos'):
					per = Permission.objects.get(id = x)
					gp.permissions.add(per)
				messages.success(request, 'Grupo editado con éxito')
			except Exception as e:
				print (e)
				messages.error(request, 'Ocurrió un problema al editar grupo')
		return redirect('grupos_listado')
	else:
		gp = Group.objects.get(pk = id)
		group = AuthGroupExtended.objects.get(pk = gp.pk)
		listado_permisos = Permission.objects.all().order_by('-content_type')
		ctx = {
			'listado_permisos':listado_permisos,
			'gp':gp,
			'group': group
		}
		return render(request, 'grupos_editar.html', ctx )

@login_required()
def usuarios_listado(request):
	listado = User.objects.values('id', 'username', 'first_name', 'last_name', 'email', 'is_active').all().order_by('-is_active')
	ctx = {
		'listado':listado,
	}
	return render(request, 'usuarios_listado.html', ctx)

@login_required()
def usuarios_detalle(request, id):
	if request.is_ajax():
		import json
		codigo = request.GET['codigo']
		try:
			user = User.objects.get(pk = codigo)
			user.is_active = False if user.is_active else True
			user.save()
			print(user.is_active)
			data = json.dumps({
                            'estado': user.is_active,
                        })
		except Exception as e:
			data = json.dumps({
                    'estado': '' ,
                })

		return HttpResponse(data, content_type='application/json')

	if request.POST:
		pass
	else:
		try:
			us = User.objects.get(pk = id)
		except Exception as e:
			messages.error(request, 'Ocurrió un problema al obtener usuario')
			return redirect('usuarios_listado')
		if us.profile.auth_time_session is not None:
			hours = float(us.profile.auth_time_session) / 60
			hours = "{0:.2f}".format(hours)
		else:
			hours = 0

		listadpoRpt = list(Bitacora.objects.filter(user = us.pk).values(
			'reporte__reporte_nombre', 'reporte__subtema__subtema_nombre',
			'bit_last_date', 'bit_counter'
			).order_by('reporte__subtema__subtema_nombre'))
		ctx = {
			'us': us,
			'hours':hours,
			'listadpoRpt':listadpoRpt 
		}
		return render(request, 'usuarios_detalle.html', ctx)

@login_required()
@transaction.atomic
def usuarios_reset_pwd(request, id):
	if request.POST:
		user = User.objects.get(pk = id)
		form = AdminPasswordChangeForm(user, request.POST)

		if form.is_valid():
			form.save() 
			messages.success(request, 'Cambio de contraseña realizado con éxito')

		else:
			messages.error(request, 'No se pudo realizar el cambio de la contraseña')
			try:
				user = User.objects.get(pk = id)
				form = AdminPasswordChangeForm(user)
			except Exception as e:
				print(e)
				messages.error(request, 'Ocurrió un problema al obtener usuario')
				return redirect('usuarios_listado')
			ctx = {
				'form': form,
				'user': user, 
			}
			return render(request, 'usuarios_reset_pwd.html', ctx)

		return redirect(reverse('usuarios_detalle', kwargs={'id': id}))

	else:
		try:
			user = User.objects.get(pk = id)
			form = AdminPasswordChangeForm(user)
		except Exception as e:
			print(e)
			messages.error(request, 'Ocurrió un problema al obtener usuario')
			return redirect('usuarios_listado')
		ctx = {
			'form': form,'user': user, 
		}
		return render(request, 'usuarios_reset_pwd.html', ctx)




# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import *
#from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, Group, Permission
#from m_generales.models import *
import os 
from django.conf import settings
from django.db.models import Count, Sum 
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.humanize.templatetags.humanize import *
#from django.db import connection
#import ldap
#from crmFincesa.settings import EN_SERVIDOR
#from django.utils.encoding import force_unicode

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
		listado_permisos = Permission.objects.all().order_by('-content_type')
		ctx = {
			'listado_permisos':listado_permisos,
			'gp':gp
		}
		return render(request, 'grupos_editar.html', ctx )


# -*- coding: utf-8 -*- 
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import *  
#from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User, Group
from m_generales.models import *
import os 
from django.conf import settings
from django.db.models import Count, Sum 
from django.contrib import messages
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db import connection 
from django.contrib.humanize.templatetags.humanize import *
from m_temas.models import *
from m_generales.forms import SignUpForm
from savio.tokens import account_activation_token, account_reset_token
from savio.send_email import email_activacion, email_contacto, email_resetPwd
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

def dictfetchall(cursor):
	columns = [col[0] for col in cursor.description]
	return [
		dict(zip(columns, row))
		for row in cursor.fetchall()
	] 

def inicio(request):
	listado_metas = list(TmsTema.objects.values(
			'tema_id',
			'tema_nombre',
			'tema_descripcion',
			'tema_estado'
		).filter(tema_estado = True))
	ctx = {
		'listado_metas':listado_metas,
	}
	return render(request, 'inicio.html', ctx)

def salir(request):
	logout(request)
	return redirect('inicio')

def suscribirse(request):
	if request.is_ajax():
		import json
		listado = list(GralMunicipios.objects.values('mun_id', 'mun_nombre').filter(depto = request.GET['codigo']))
		data = json.dumps({
			'listado':listado,
			})
		return HttpResponse(data, content_type='application/json')

	if request.method == 'POST':
		import random
		import string
		form = SignUpForm(request.POST) 
		if form.is_valid():
			user = form.save()
			user.refresh_from_db() # load the profile instance created by the signal
			user.is_active = False
			user.email = user.username
			user.profile.auth_email_confirmed = False#GralMunicipios.objects.get(pk = request.POST['mun'])
			user.save()
 			
			current_site = get_current_site(request)
			subject = 'Savio | activación de cuenta'

			toRange = 15
			x1 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(toRange))
			x2 = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(toRange))
			codigo_con = str(x1)+''+str(user.pk)+''+str(x2)

			message = render_to_string('extras/activacionCuenta.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': codigo_con,
				'token': account_activation_token.make_token(user),
			})
			email_activacion(user.username, subject, message)
			messages.info(request, 'Se ha enviado un mensaje a tu correo electrónico')
			return redirect('inicio')
		else:
			return render(request, 'suscribirse.html', {'form': form})

	else:
		form = SignUpForm()
	return render(request, 'suscribirse.html', {'form': form})
  
def reset_password(request):
	if request.POST:
		try:
			user = User.objects.get(username = request.POST['username'])
		except Exception as e:
			messages.danger(request, 'No se pudo obtener usuario')
			return redirect('login')
		
		current_site = get_current_site(request)
		subject = 'Savio | Recuperación de cuenta'
		message = render_to_string('extras/resetPassword.html', {
			'user': user,
			'domain': current_site.domain,
			'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			'token': account_reset_token.make_token(user),
		})
		email_resetPwd(user.username, subject, message)
		messages.info(request, 'Se ha enviado un mensaje a tu correo electrónico')
		return redirect('login')

def activate(request, uidb64, token):
	try:
		uid =  uidb64[15:][:-15]
		user = User.objects.get(pk=uid)
	except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
		print (e)
		user = None

	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.profile.email_confirmed = True
		user.save()
		messages.success(request, 'Cuenta fue activada con éxito')
		auth_login(request, user)
		return redirect('reportes')
	else:
		return  redirect('inicio')

def quien_soy(request):
	ctx={}
	return render(request, 'quien_soy.html', ctx)

def contacto(request):

	if request.POST:
		import datetime as dt

		subject = 'Savio | Solicitud de Contacto'
		message = render_to_string('extras/contactoEmail.html', {
			'nombre': request.POST['cltNombre'],
			'asunto': request.POST['cltAsunto'],
			'correo': request.POST['cltEmail'],
			'comentario': request.POST['cltComentario'],
			'fecha': dt.datetime.today().strftime('%Y-%m-%d %H:%M')
		})
		email_contacto('franklin.banegas@bi-dss.com', subject, message)
		messages.info(request, 'Muchas gracias, alguien de nuestro equipo se pondrá en contacto contigo')
		return redirect('inicio')
	ctx={}
	return render(request, 'contacto.html', ctx)

@login_required()
def reportes(request):
	listado_metas = list(TmsTema.objects.values(
			'tema_id',
			'tema_nombre',
			'tema_descripcion',
			'tema_estado'
		).filter(tema_estado = True))
	ctx = {
		'listado_metas':listado_metas,
	}
	return render(request, 'reportes.html', ctx)

def handler404(request, *args, **argv):
	return render(request, 'paginasErrores/404.html', {})

def handler500(request, *args, **argv):
	return render(request, 'paginasErrores/500.html', {})

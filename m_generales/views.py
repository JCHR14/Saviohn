# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.http import *
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.contrib.auth.models import User, Group
from m_generales.models import *
import os
from django.db.models import Count, Sum
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import *
from m_temas.models import *
from m_generales.forms import SignUpForm
from savio.tokens import account_activation_token, account_reset_token
from savio.send_email import email_activacion, email_contacto, email_resetPwd
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import logging
import datetime as dt
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

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
			'tema_logo',
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
			'tema_logo',
			'tema_estado'
		).filter(tema_estado = True))
	ctx = {
		'listado_metas':listado_metas,
	}
	return render(request, 'reportes.html', ctx)

# for logging - define "error" named logging handler and logger in settings.py
error_log=logging.getLogger('error')

@receiver(user_logged_in)
def log_user_logged_in(sender, user, request, **kwargs):
	try:
		AuthBitacoraSession.objects.create(
			user = user,
			bit_login_time = dt.datetime.now(),
			bit_activo =  True,
			bit_host = request.META['HTTP_HOST']
		)
	except Exception as e:
		error_log.error("log_user_logged_in request: %s, error: %s" % (request, e))

@receiver(user_logged_out)
def log_user_logged_out(sender, user, request, **kwargs):
	try:
		bita = AuthBitacoraSession.objects.filter(user = user.pk, bit_activo = True).last()
		bita.bit_logout_time = dt.datetime.now()
		bita.bit_activo =  False
		bita.save()
		resultado = dt.datetime.now() -  bita.bit_login_time
		minutos = float(resultado.total_seconds() / 60)
		pro = profile.objects.get(pk = user.pk)
		acum = pro.auth_time_session
		if acum is not None:
			total = float(acum) + minutos
		else:
			total = minutos
		total = "{0:.2f}".format(total)
		pro.auth_time_session = total
		pro.save()
	except Exception as e:
		error_log.error("log_user_logged_out request: %s, error: %s" % (request, e))

def handler404(request, *args, **argv):
	return render(request, 'paginasErrores/404.html', {})

def handler500(request, *args, **argv):
	return render(request, 'paginasErrores/500.html', {})

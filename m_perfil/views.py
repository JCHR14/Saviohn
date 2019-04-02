# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
from django.shortcuts import render, redirect
from django.http import *
from django.template import RequestContext
#from django.urls import reverse
from m_generales.models import *
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.humanize.templatetags.humanize import *
from django.contrib import messages
from django.conf import settings
from django.db.models import Count, Sum
from django.db import transaction

@login_required()
def perfil(request):
	ctx = {}
	return render(request, 'perfil.html', ctx)

@login_required()
@transaction.atomic
def change_password(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Contraseña actualizada correctamente')
			return redirect('perfil')
		else:
			messages.error(request, 'No se pudo actualizar contraseña')
			return redirect('change_password')
	else:
		form = PasswordChangeForm(request.user)
	return render(request, 'change_password.html', {
		'form': form
	})


@login_required()
def editar_perfil(request):
	if request.POST:
		try:
			us = User.objects.get(pk = request.user.id)
			us.first_name = request.POST['first_name'][:30]
			us.last_name = request.POST['last_name'][:150]
			us.save()
			pro = profile.objects.filter(auth=us.pk).update(auth_birth_date=request.POST['auth_birth_date'])
			messages.success(request, 'Perfil actualizada correctamente')
			return redirect('perfil')
		except Exception as e:
			print (e)
			messages.error(request, 'No se pudo editar perfil')
			return redirect('perfil')
	else:
		ctx = {}
		return render(request, 'editar_perfil.html', ctx )

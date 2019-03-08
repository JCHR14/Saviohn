# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os 
from django.shortcuts import render, redirect
from django.http import * 
from django.template import RequestContext
#from django.urls import reverse
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
#from m_generales.models import *
#from django.contrib.auth.forms import PasswordChangeForm
#from django.shortcuts import render_to_response
#from django.db import connection
#from plan.global_utils_function import generar_pass, email
#from django.utils.encoding import force_unicode
#from m_temas.models import *

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

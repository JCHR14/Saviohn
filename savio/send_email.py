# -*- coding: utf-8 -*-
from savio.settings import USERNAME_MAIL, PASSWORD_MAIL, SERVER_SMTP


def email_activacion( emailTo, suject, body):
	from io import StringIO
	from django.template.loader import render_to_string
	from django.template import Context, Template
	from email import encoders
	import smtplib
	import email
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart
	#from email.MIMEBase import MIMEBase
	#from email.Encoders import encode_base64
	#from email.mime.multipart import MIMEMultipart
	msg = MIMEMultipart()
	msg['Subject'] = suject
	msg['To'] = emailTo
	msg['From'] = USERNAME_MAIL
	context = Context({})
	template = Template(body)
	msg.attach(MIMEText(template.render(context).encode('utf-8'), 'html', 'utf-8'))
	server = smtplib.SMTP(str(SERVER_SMTP))
	server.starttls()
	server.ehlo()
	server.login(USERNAME_MAIL, PASSWORD_MAIL)
	server.sendmail(USERNAME_MAIL, emailTo, msg.as_string())
	server.quit()

def email_contacto( emailTo, suject, body):
	from django.template.loader import render_to_string
	from django.template import Context, Template
	from email import encoders
	import smtplib
	from email.mime.text import MIMEText
	from email.mime.multipart import MIMEMultipart
	from email.MIMEBase import MIMEBase
	from email.Encoders import encode_base64
	msg = MIMEMultipart()
	msg['Subject'] = suject
	msg['To'] = emailTo
	msg['From'] = USERNAME_MAIL
	context = Context({})
	template = Template(body)
	msg.attach(MIMEText(template.render(context).encode('utf-8'), 'html', 'utf-8'))
	server = smtplib.SMTP(str(SERVER_SMTP))
	server.starttls()
	server.ehlo()
	server.login(USERNAME_MAIL, PASSWORD_MAIL)
	server.sendmail(USERNAME_MAIL, emailTo, msg.as_string())
	server.quit()



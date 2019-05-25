from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from m_temas.models import TmsReporte
# Create your models here.  
class profile(models.Model):
    auth = models.OneToOneField(User, models.DO_NOTHING, db_column='auth', primary_key=True)
    auth_email_confirmed = models.BooleanField(default=False)
    auth_birth_date = models.DateField(null=True, blank=True)
    auth_change_pass = models.NullBooleanField(default=False)
    auth_country = models.CharField(max_length=50, blank=True, null=True)
    auth_city = models.CharField(max_length=50, blank=True, null=True)
    auth_time_session = models.CharField(max_length=20, blank=True, null=True)
    auth_host = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_profile'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(auth=instance)
    instance.profile.save()

class Bitacora(models.Model):
    bit_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)
    reporte = models.ForeignKey(TmsReporte, models.DO_NOTHING, blank=True, null=True)
    bit_last_date = models.DateTimeField(blank=True, null=True)
    bit_counter = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'bitacora'
 
class AuthBitacoraSession(models.Model):
    bit_id = models.AutoField(primary_key=True)
    bit_login_time = models.DateTimeField(blank=True, null=True)
    bit_logout_time = models.DateTimeField(blank=True, null=True)
    bit_host = models.CharField(max_length=100, blank=True, null=True)
    bit_activo = models.BooleanField(blank=True, null=True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_bitacora_session'


class BitacoraBusqUser(models.Model):
    busq_id = models.AutoField(primary_key=True)
    busq_query = models.CharField(max_length=50, blank=True, null=True)
    busq_fecha = models.DateTimeField(blank=True, null=True, auto_now = True)
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bitacora_busq_user'

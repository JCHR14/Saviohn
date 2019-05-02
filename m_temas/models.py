from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

def upload_logo(instance, filename):
    return 'temas/{0}/{1}'.format(instance.user_creador, filename.encode('ascii', 'ignore'))
 
class TmsReporte(models.Model):
    reporte_id = models.AutoField(primary_key=True)
    reporte_nombre = models.CharField(max_length=50, blank=True, null=True)
    reporte_descripcion = models.CharField(max_length=500, blank=True, null=True)
    reporte_estado = models.BooleanField(blank=True, null=True)
    reporte_gratuito = models.BooleanField(blank=True, null=True)
    reporte_is_principal = models.BooleanField(blank=True, null=True)
    reporte_is_secundario = models.BooleanField(blank=True, null=True)
    reporte_referencias = models.CharField(max_length=5000, blank=True, null=True)
    reporte_iframe = models.CharField(max_length=5000, blank=True, null=True)
    reporte_tags = models.CharField(max_length=100, blank=True, null=True)
    reporte_user = models.CharField(max_length=100, blank=True, null=True)
    reporte_pwd = models.CharField(max_length=100, blank=True, null=True)
    reporte_need_auth = models.BooleanField(blank=True, null=True)
    subtema = models.ForeignKey('TmsSubtema', models.DO_NOTHING, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True, auto_now=True)
    user_creador = models.ForeignKey(User, models.DO_NOTHING, db_column='user_creador', blank=True, null=True)
    user_modificador = models.ForeignKey(User, models.DO_NOTHING, db_column='user_modificador', blank=True, null=True, related_name='reporte_modificador')
 
    class Meta:
        managed = False
        db_table = 'tms_reporte'


class TmsSubtema(models.Model):
    subtema_id = models.AutoField(primary_key=True)
    subtema_nombre = models.CharField(max_length=50, blank=True, null=True)
    subtema_subnombre = models.CharField(max_length=50, blank=True, null=True)
    subtema_descripcion = models.CharField(max_length=500, blank=True, null=True)
    subtema_tags = models.CharField(max_length=500, blank=True, null=True)
    subtema_fuente = models.CharField(max_length=500, blank=True, null=True)
    subtema_estado = models.BooleanField(blank=True, null=True)
    tema = models.ForeignKey('TmsTema', models.DO_NOTHING, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True, auto_now=True)
    user_creador = models.ForeignKey(User, models.DO_NOTHING, db_column='user_creador', blank=True, null=True)
    user_modificador = models.ForeignKey(User, models.DO_NOTHING, db_column='user_modificador', blank=True, null=True, related_name='subtema_modificador')
    class Meta:
        managed = False
        db_table = 'tms_subtema'


class TmsTema(models.Model):
    tema_id = models.AutoField(primary_key=True)
    tema_nombre = models.CharField(max_length=20, blank=True, null=True)
    tema_descripcion = models.CharField(max_length=100, blank=True, null=True)
    tema_estado = models.BooleanField(blank=True, null=True)
    tema_logo = models.FileField(db_column='tema_logo', upload_to=upload_logo)

    fecha_creacion = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True, auto_now=True)
    user_creador = models.ForeignKey(User, models.DO_NOTHING, db_column='user_creador', blank=True, null=True)
    user_modificador = models.ForeignKey(User, models.DO_NOTHING, db_column='user_modificador', blank=True, null=True, related_name='tema_modificador')

    class Meta:
        managed = False
        db_table = 'tms_tema'




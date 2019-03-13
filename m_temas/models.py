from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

def upload_logo(instance, filename):
    return 'reportes/{0}/{1}'.format(instance.user_creador, filename.encode('ascii', 'ignore'))

class TmsReporte(models.Model):
    reporte_id = models.AutoField(primary_key=True)
    reporte_nombre = models.CharField(max_length=50, blank=True, null=True)
    reporte_descripcion = models.CharField(max_length=100, blank=True, null=True)
    reporte_estado = models.BooleanField(blank=True, null=True)
    reporte_gratuito = models.BooleanField(blank=True, null=True)
    reporte_url = models.CharField(max_length=5000, blank=True, null=True)
    reporte_user = models.CharField(max_length=100, blank=True, null=True)
    reporte_pwd = models.CharField(max_length=100, blank=True, null=True)
    reporte_need_auth = models.BooleanField(blank=True, null=True)
    reporte_logo = models.FileField(db_column='reporte_logo', upload_to=upload_logo)
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
    tema_estado = models.BooleanField(blank=True, null=True)
    tema_descripcion = models.CharField(max_length=100, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)
    user_creador = models.ForeignKey(User, models.DO_NOTHING, db_column='user_creador', blank=True, null=True)
    user_modificador = models.ForeignKey(User, models.DO_NOTHING, db_column='user_modificador', blank=True, null=True, related_name='tema_modificador')

    class Meta:
        managed = False
        db_table = 'tms_tema'


'''
class GralSubtema(models.Model):
    subtema_id = models.AutoField(primary_key=True)
    subtema_nombre = models.CharField(max_length=20, blank=True, null=True)
    subtema_estado = models.NullBooleanField()
    tema = models.ForeignKey('GralTema', models.DO_NOTHING, blank=True, null=True)
    subtema_powerbi = models.NullBooleanField()
    subtema_powerbi_link = models.CharField(max_length=8000, blank=True, null=True)
    subtema_opcion2 = models.NullBooleanField()
    subtema_opcion2_link = models.CharField(max_length=8000, blank=True, null=True)
    subtema_opcion3 = models.NullBooleanField()
    subtema_opcion3_link = models.CharField(max_length=8000, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)
    user_creador = models.ForeignKey(User, models.DO_NOTHING, db_column='user_creador', blank=True, null=True)
    user_modificador = models.ForeignKey(User, models.DO_NOTHING, db_column='user_modificador', blank=True, null=True, related_name='subtema_modificador')

    class Meta:
        managed = False
        db_table = 'gral_subTema'


class GralTema(models.Model):
    tema_id = models.AutoField(primary_key=True)
    tema_nombre = models.CharField(max_length=20, blank=True, null=True)
    tema_estado = models.NullBooleanField(default=True)
    tema_descripcion = models.CharField(max_length=100, blank=True, null=True)
    user_creador = models.ForeignKey(User, models.DO_NOTHING, db_column='user_creador', blank=True, null=True)
    user_modificador = models.ForeignKey(User, models.DO_NOTHING, db_column='user_modificador', blank=True, null=True, related_name='_modificador')
    fecha_creacion = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        managed = False
        db_table = 'gral_tema'
'''

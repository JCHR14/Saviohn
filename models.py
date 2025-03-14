# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthProfile(models.Model):
    auth = models.ForeignKey('AuthUser', models.DO_NOTHING, db_column='auth', primary_key=True)
    auth_email_confirmed = models.BooleanField(blank=True, null=True)
    auth_birth_date = models.DateField(blank=True, null=True)
    auth_change_pass = models.BooleanField(blank=True, null=True)
    mun = models.ForeignKey('GralMunicipios', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_profile'


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class GralDepartamentos(models.Model):
    depto_id = models.CharField(primary_key=True, max_length=2)
    depto_nombre = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gral_departamentos'


class GralMunicipios(models.Model):
    mun_id = models.CharField(primary_key=True, max_length=5)
    mun_nombre = models.CharField(max_length=100, blank=True, null=True)
    depto = models.ForeignKey(GralDepartamentos, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gral_municipios'


class GralSubtema(models.Model):
    subtema_id = models.AutoField(primary_key=True)
    subtema_nombre = models.CharField(max_length=20, blank=True, null=True)
    subtema_estado = models.BooleanField(blank=True, null=True)
    tema = models.ForeignKey('TmsTema', models.DO_NOTHING, blank=True, null=True)
    subtema_powerbi = models.BooleanField(blank=True, null=True)
    subtema_powerbi_link = models.CharField(max_length=8000, blank=True, null=True)
    subtema_opcion2 = models.BooleanField(blank=True, null=True)
    subtema_opcion2_link = models.CharField(max_length=8000, blank=True, null=True)
    subtema_opcion3 = models.BooleanField(blank=True, null=True)
    subtema_opcion3_link = models.CharField(max_length=8000, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)
    user_creador = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_creador', blank=True, null=True)
    user_modificador = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_modificador', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'gral_subTema'


class TmsReporte(models.Model):
    reporte_id = models.AutoField(primary_key=True)
    reporte_nombre = models.CharField(max_length=50, blank=True, null=True)
    reporte_descripcion = models.CharField(max_length=100, blank=True, null=True)
    reporte_estado = models.BooleanField(blank=True, null=True)
    reporte_gratuito = models.BooleanField(blank=True, null=True)
    reporte_url = models.CharField(max_length=5000, blank=True, null=True)
    reporte_logo = models.CharField(max_length=500, blank=True, null=True)
    subtema = models.ForeignKey('TmsSubtema', models.DO_NOTHING, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)
    user_creador = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_creador', blank=True, null=True)
    user_modificador = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_modificador', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tms_reporte'


class TmsSubtema(models.Model):
    subtema_id = models.AutoField(primary_key=True)
    subtema_nombre = models.CharField(max_length=50, blank=True, null=True)
    subtema_estado = models.BooleanField(blank=True, null=True)
    tema = models.ForeignKey('TmsTema', models.DO_NOTHING, blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)
    fecha_modificacion = models.DateTimeField(blank=True, null=True)
    user_creador = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_creador', blank=True, null=True)
    user_modificador = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_modificador', blank=True, null=True)

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
    user_creador = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_creador', blank=True, null=True)
    user_modificador = models.ForeignKey(AuthUser, models.DO_NOTHING, db_column='user_modificador', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tms_tema'

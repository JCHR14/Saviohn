# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthBitacoraSession(models.Model):
    bit_id = models.AutoField(primary_key=True)
    bit_login_time = models.DateTimeField(blank=True, null=True)
    bit_logout_time = models.DateTimeField(blank=True, null=True)
    bit_host = models.CharField(max_length=100, blank=True, null=True)
    bit_activo = models.BooleanField(blank=True, null=True)
    user = models.ForeignKey('AuthUser', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_bitacora_session'

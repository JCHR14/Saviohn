# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroupExtended(models.Model):
    group = models.ForeignKey('AuthGroup', models.DO_NOTHING, primary_key=True)
    group_for_client = models.BooleanField(blank=True, null=True)
    group_detalle = models.CharField(max_length=500, blank=True, null=True)
    group_sub_detalle = models.CharField(max_length=500, blank=True, null=True)
    group_need_price = models.BooleanField(blank=True, null=True)
    group_price_month = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    group_price_anual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    group_price_detalle = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group_extended'

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class profile(models.Model):
    auth = models.OneToOneField(User, models.DO_NOTHING, db_column='auth', primary_key=True)
    auth_email_confirmed = models.BooleanField(default=False)
    auth_birth_date = models.DateField(null=True, blank=True)
    auth_change_pass = models.NullBooleanField(default=False)
    mun = models.ForeignKey('GralMunicipios', models.DO_NOTHING, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'auth_profile'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        profile.objects.create(auth=instance)
    instance.profile.save()


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

 ###############################################################################################
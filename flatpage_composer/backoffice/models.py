from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
class LoginLog(models.Model):

	id = models.AutoField(db_column='ID', primary_key=True)
	created = models.DateTimeField(db_column='CREATED', auto_now_add=True, blank=True)
	ip_address = models.CharField(db_column='IP_ADDRESS', max_length=64, blank=True)

	class Meta:
		db_table = 'LOGIN_LOG'
		ordering = ["id"]
		verbose_name = _("Login Log") 
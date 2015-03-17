from django.db import models


class UserProfile(models.Model):
    amazonId = models.CharField(max_length=255, blank=False, null=False, default='')

class Gift(models.Model):
    owner = models.ForeignKey(UserProfile)
    name = models.CharField(max_length=255, blank=False, null=False, default='')
    url = models.CharField(max_length=255, blank=False, null=False, default='') 
    price = models.FloatField(blank=False, null=False, default='0.0')
    def __unicode__(self):
        return self.name

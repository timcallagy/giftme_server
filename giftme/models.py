from django.db import models

class Gift(models.Model):
    owner_id = models.CharField(max_length=255, blank=False, null=False, default='')
    name = models.CharField(max_length=255, blank=False, null=False, default='')
    url = models.CharField(max_length=255, blank=False, null=False, default='') 
    price = models.FloatField(blank=False, null=False, default='0.0')
    crowdfunded = models.FloatField(blank=True, null=True, default='0')
    def __unicode__(self):
        return self.name

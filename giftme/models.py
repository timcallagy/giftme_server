import datetime
from django.db import models

class Gift(models.Model):
    owner_id = models.CharField(max_length=255, blank=False, null=False, default='')
    name = models.CharField(max_length=255, blank=False, null=False, default='')
    url = models.CharField(max_length=1020, blank=False, null=False, default='') 
    pic = models.CharField(max_length=255, blank=False, null=False, default='') 
    price = models.FloatField(blank=False, null=False, default='0.0')
    crowdfunded = models.FloatField(blank=True, null=True, default='0')
    def __unicode__(self):
        return self.name

class Contribution(models.Model):
    gift = models.ForeignKey(Gift)
    gift_name = models.CharField(max_length=255, blank=False, null=False, default='')
    contributor_id = models.CharField(max_length=255, blank=False, null=False, default='')
    contributor_name = models.CharField(max_length=255, blank=False, null=False, default='')
    contributed_to = models.CharField(max_length=255, blank=False, null=False, default='')
    amount = models.FloatField(blank=True, null=True, default='0')
    message = models.CharField(max_length=255, blank=True, null=True, default='')
    contribution_date = models.DateTimeField(blank=False, null=False, default=datetime.datetime.now())
    stripe_charge = models.CharField(max_length=255, blank=True, null=True, default='')
    def __unicode__(self):
        description = "$" + str(int(self.amount)) + " for " + self.gift_name + " from " + self.contributor_name
        return description

from datetime import datetime, date
from django.db import models

class Gift(models.Model):
    owner_id = models.CharField(max_length=255, blank=False, null=False, default='')
    owner_name = models.CharField(max_length=255, blank=False, null=False, default='')
    name = models.CharField(max_length=255, blank=False, null=False, default='')
    url = models.CharField(max_length=1020, blank=False, null=False, default='') 
    pic = models.CharField(max_length=255, blank=False, null=False, default='') 
    price = models.FloatField(blank=False, null=False, default='0.0')
    crowdfunded = models.FloatField(blank=True, null=True, default='0')
    added_date =  models.DateTimeField(blank=False, null=False, default=datetime.now())
    def __unicode__(self):
        description = self.owner_name + " added '" + self.name + "' to their wishlist"
        return description

class Contribution(models.Model):
    gift = models.ForeignKey(Gift)
    gift_name = models.CharField(max_length=255, blank=False, null=False, default='')
    contributor_id = models.CharField(max_length=255, blank=False, null=False, default='')
    contributor_name = models.CharField(max_length=255, blank=False, null=False, default='')
    contributed_to = models.CharField(max_length=255, blank=False, null=False, default='')
    contributed_to_name = models.CharField(max_length=255, blank=False, null=False, default='')
    amount = models.FloatField(blank=True, null=True, default='0')
    message = models.CharField(max_length=255, blank=True, null=True, default='')
    contribution_date = models.DateTimeField(blank=False, null=False, default=datetime.now())
    stripe_charge = models.CharField(max_length=255, blank=True, null=True, default='')
    def __unicode__(self):
        description = self.contributor_name + " gave US$ " + str(int(self.amount)) + " to " + self.contributed_to_name + " for " + self.gift_name
        return description

class FacebookSession(models.Model):
    userID = models.CharField(max_length=255, blank=False, null=False, default='')
    name = models.CharField(max_length=255, blank=False, null=False, default='')
    email = models.CharField(max_length=255, blank=False, null=False, default='')
    receiveEmails = models.BooleanField(blank=True, default=True)
    accessToken = models.CharField(max_length=1020, blank=False, null=False, default='') 
    expiryTime = models.DateTimeField(blank=False, null=False, default=datetime.now())
    birthday = models.DateTimeField(blank=True, null=True, default=date(1900, 01, 01))
    joined_date = models.DateTimeField(blank=False, null=False, default=datetime.now())
    def __unicode__(self):
        return self.name + "'s session"

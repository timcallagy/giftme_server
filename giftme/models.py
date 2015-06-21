from datetime import datetime, date
from numpy import asarray
from django.db import models

amounts = asarray([5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200, 250, 300, 350, 400, 450, 500])

class Gift(models.Model):
    owner_id = models.CharField(max_length=255, blank=False, null=False, default='')
    owner_name = models.CharField(max_length=255, blank=False, null=False, default='')
    name = models.CharField(max_length=255, blank=False, null=False, default='')
    url = models.CharField(max_length=1020, blank=False, null=False, default='') 
    pic = models.CharField(max_length=255, blank=False, null=False, default='') 
    price = models.FloatField(blank=False, null=False, default='0.0')
    description = models.CharField(max_length=5000, blank=True, null=True, default='')
    crowdfunded = models.FloatField(blank=True, null=True, default='0')
    added_date =  models.DateTimeField(blank=False, null=False, default=datetime.now())
    def __unicode__(self):
        description = self.owner_name + " added '" + self.name + "' to their wishlist"
        return description
    def formatPricesUSD(self):
        self.priceStr = 'USD $' + '{:.2f}'.format(self.price)
        self.crowdfundedStr = 'USD $' + '{:.2f}'.format(self.crowdfunded)
    def formatPricesEUR(self, rate):
        self.priceStrEUR = 'EUR ' + '{:.2f}'.format(self.price*rate)
        self.crowdfundedStrEUR = 'EUR ' + '{:.2f}'.format(self.crowdfunded*rate)
    def add_valid_amountsUSD(self):
        self.remaining = round(self.price - self.crowdfunded,2)
        print("REMAINING:")
        print(self.remaining)
        valid_amounts = list(amounts[amounts <= self.remaining])
        if len(valid_amounts) > 0 and valid_amounts[-1] < (self.remaining) : valid_amounts.append(self.remaining)
        self.amounts = valid_amounts
    def add_valid_amountsEUR(self, rate):
        self.remainingEUR = round((self.price - self.crowdfunded)*rate,2)
        valid_amounts = list(amounts[amounts <= self.remainingEUR])
        if len(valid_amounts) > 0 and valid_amounts[-1] < (self.remainingEUR) : valid_amounts.append(self.remainingEUR)
        self.amountsEUR = valid_amounts


class Contribution(models.Model):
    gift = models.ForeignKey(Gift)
    gift_name = models.CharField(max_length=255, blank=False, null=False, default='')
    gift_pic = models.CharField(max_length=255, blank=False, null=False, default='')
    contributor_id = models.CharField(max_length=255, blank=False, null=False, default='')
    contributor_name = models.CharField(max_length=255, blank=False, null=False, default='')
    contributed_to = models.CharField(max_length=255, blank=False, null=False, default='')
    contributed_to_name = models.CharField(max_length=255, blank=False, null=False, default='')
    amount = models.FloatField(blank=True, null=True, default='0')
    message = models.CharField(max_length=5000, blank=True, null=True, default='')
    contribution_date = models.DateTimeField(blank=False, null=False, default=datetime.now())
    stripe_charge = models.CharField(max_length=255, blank=True, null=True, default='')
    def __unicode__(self):
        description = self.contributor_name + " gave US$ " + str(int(self.amount)) + " to " + self.contributed_to_name + " for '" + self.gift_name + "'"
        return description

class FacebookSession(models.Model):
    userID = models.CharField(max_length=255, blank=False, null=False, default='')
    name = models.CharField(max_length=255, blank=False, null=False, default='')
    email = models.CharField(max_length=255, blank=False, null=False, default='')
    gender = models.CharField(max_length=255, blank=False, null=False, default='')
    receiveEmails = models.BooleanField(blank=True, default=True)
    accessToken = models.CharField(max_length=1020, blank=False, null=False, default='') 
    expiryTime = models.DateTimeField(blank=False, null=False, default=datetime.now())
    birthday = models.DateTimeField(blank=True, null=True, default=date(1900, 01, 01))
    joined_date = models.DateTimeField(blank=False, null=False, default=datetime.now())
    def __unicode__(self):
        return self.name + "'s session"

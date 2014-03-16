import requests
from django.db import models


class Account(models.Model):
    phone_number = models.CharField(max_length=20)

    def __unicode__(self):
        return self.phone_number

    def get_balance(self):
        return sum(wallet.get_balance() for wallet in self.wallets.all())


class Wallet(models.Model):
    account = models.ForeignKey(Account, related_name='wallets')
    guid = models.CharField(max_length=36)
    main_password = models.CharField(max_length=100)

    def __unicode__(self):
        return u'{}: {}'.format(self.account, self.guid)

    def get_balance(self):
        response = requests.get(
            'https://blockchain.info/merchant/{}/balance'.format(self.guid),
            params={'password': self.main_password},
        )
        data = response.json()
        if 'error' in data:
            raise Exception(data['error'])
        return data['balance']

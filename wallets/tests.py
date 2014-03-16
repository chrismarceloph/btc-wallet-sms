import httpretty
from django.core.urlresolvers import reverse
from django.test import TestCase
from .models import Account, Wallet


@httpretty.activate
class WalletModelsTest(TestCase):
    def setUp(self):
        self.account = Account.objects.create(phone_number='+19081000000')

    def test_account_balance(self):
        wallet_1 = Wallet.objects.create(account=self.account, guid='59fee004-0115-4861-8e4a-7f8af3ba31fb', main_password='password')
        httpretty.register_uri(
            httpretty.GET, 'https://blockchain.info/merchant/{}/balance?password={}'.format(wallet_1.guid, wallet_1.main_password),
            body='{"balance": 1000000}', content_type='application/json'
        )
        wallet_2 = Wallet.objects.create(account=self.account, guid='59fee004-0115-4861-8e4a-7f8af3ba31f2', main_password='password')
        httpretty.register_uri(
            httpretty.GET, 'https://blockchain.info/merchant/{}/balance?password={}'.format(wallet_2.guid, wallet_2.main_password),
            body='{"balance": 500000}', content_type='application/json'
        )
        self.assertEquals(1500000, self.account.get_balance())

    def test_wallet_balance(self):
        wallet_1 = Wallet.objects.create(account=self.account, guid='59fee004-0115-4861-8e4a-7f8af3ba31fb', main_password='password')
        httpretty.register_uri(
            httpretty.GET, 'https://blockchain.info/merchant/{}/balance?password={}'.format(wallet_1.guid, wallet_1.main_password),
            body='{"balance": 1000000}', content_type='application/json'
        )
        self.assertEquals(1000000, wallet_1.get_balance())


class WalletViewsTest(TestCase):
    def test_blank_message(self):
        response = self.client.post(reverse('receive-sms'), body='+19081000000')
        self.assertIn(response.content, 'Sorry')

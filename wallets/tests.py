import httpretty
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from .models import Account, Wallet
from .views import ReceiveSMSView


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


@httpretty.activate
class WalletViewsTest(TestCase):
    def test_add_wallet_invalid(self):
        guid = '59fee004-0115-4861-8e4a-7f8af3ba31fb'
        main_password = 'password'
        view = ReceiveSMSView()
        view.check_wallet = lambda x, y: False
        message = view.add_wallet('+19081000000', guid, main_password)
        self.assertIn('Welcome', str(message))
        self.assertIn('Sorry', str(message))

    def test_add_wallet_valid(self):
        guid = '59fee004-0115-4861-8e4a-7f8af3ba31fb'
        main_password = 'password'

        view = ReceiveSMSView()
        view.check_wallet = lambda x, y: True
        message = view.add_wallet('+19081000000', guid, main_password)
        self.assertIn('Welcome', str(message))
        self.assertIn('successfully', str(message))
        message = view.add_wallet('+19081000000', guid, main_password)
        self.assertNotIn('Welcome', str(message))
        self.assertIn('already', str(message))

    def test_check_wallet(self):
        guid = '59fee004-0115-4861-8e4a-7f8af3ba31fb'
        main_password = 'password'
        httpretty.register_uri(
            httpretty.GET, 'https://blockchain.info/merchant/{}/balance?password={}'.format(guid, main_password),
            body='{"balance": 1000000}', content_type='application/json'
        )

        view = ReceiveSMSView()
        self.assertTrue(view.check_wallet(guid, main_password))

    def test_make_response(self):
        view = ReceiveSMSView()
        response = view.make_response('Hello!')
        self.assertIn('Hello!', str(response))


class WalletIntegrationTest(TestCase):
    @override_settings(DEBUG=True)
    def test_blank_message(self):
        response = self.client.post(reverse('receive-sms'), {'From': '+19081000000', 'Body': ''})
        self.assertIn('Sorry', response.content)

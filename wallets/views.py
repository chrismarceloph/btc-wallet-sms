from twilio.twiml import Response
from django.views.generic import View
from django_twilio.decorators import twilio_view
from .models import Account, Wallet


class ReceiveSMSView(View):
    @classmethod
    def as_view(cls):
        return twilio_view(super(ReceiveSMSView, cls).as_view())

    def post(self, request, *args, **kwargs):
        phone_number = request.REQUEST.get('From')
        body = request.REQUEST.get('Body')

        message = self.process_message(phone_number, body)
        return self.make_response(message)

    def process_message(self, phone_number, body):
        parts = body.split(' ', 2)
        if parts[0] == 'ADD':
            if len(parts) < 3:
                message = 'Missing parameter. Use the format ADD [wallet address] [password]'
            else:
                message = self.add_wallet(phone_number, parts[1], parts[2])
        elif parts[0] == 'REM':
            if len(parts) < 2:
                message = 'Missing parameter. Use the format REM [wallet address]'
            else:
                message = self.remove_wallet(phone_number, parts[1])
        elif parts[0] == 'BAL':
            message = self.get_balance(phone_number)
        else:
            message = 'Sorry, I cannot understand your message. Please check your message and try again.'
        return message

    def add_wallet(self, phone_number, guid, main_password):
        parts = []
        account, created = Account.objects.get_or_create(phone_number=phone_number)
        if created:
            parts.append('Welcome to btc-wallet-sms!')

        if self.check_wallet(guid, main_password):
            wallet, created = Wallet.objects.get_or_create(account=account, guid=guid, defaults={
                'main_password': main_password
            })
            if created:
                parts.append('You have successfully added this wallet to your account.')
            else:
                parts.append('You have already added this wallet to your account before.')
        else:
            parts.append('Sorry, your parameters did not correspond to a valid wallet.')
        return ' '.join(parts)

    def check_wallet(self, guid, main_password):
        wallet = Wallet()
        wallet.guid = guid
        wallet.main_password = main_password
        try:
            wallet.get_balance()
        except Exception:
            return False
        else:
            return True

    def remove_wallet(self, phone_number, guid):
        try:
            Wallet.objects.get(account__phone_number=phone_number, guid=guid).delete()
        except Wallet.DoesNotExist:
            return 'Sorry, your parameters did not correspond to a valid wallet.'
        else:
            return 'You have successfully removed this wallet from your account.'

    def get_balance(self, phone_number):
        try:
            account = Account.objects.get(phone_number=phone_number)
        except Wallet.DoesNotExist:
            return 'Sorry, your phone number is not registered yet.'
        else:
            satoshis = account.get_balance()
            btc = satoshis / 100000000.0
            return 'Your current balance is {} Satoshis ({} BTC).'.format(satoshis, btc)

    def make_response(self, message):
        response = Response()
        response.sms(message)
        return response

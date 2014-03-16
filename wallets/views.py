from twilio.twiml import Response
from django.views.generic import View
from django_twilio.decorators import twilio_view


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
        message = 'Sorry, I cannot understand your message. Please check your message and try again.'
        return message

    def make_response(self, message):
        response = Response()
        response.sms(message)
        return response

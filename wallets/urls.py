from django.conf.urls import patterns, url
from .views import ReceiveSMSView


urlpatterns = patterns('',
    url(r'^receive-sms/$', ReceiveSMSView.as_view(), name='receive-sms'),
)

import json
import logging
from abc import ABCMeta, abstractmethod

import requests
from django.conf import settings
from twilio.rest import Client


class MessageTransport(metaclass=ABCMeta):
    def __init__(self, message):
        self.message = message

    @abstractmethod
    def send(self):
        raise NotImplementedError('All message transport subclass should implement the send method!')


class Email(MessageTransport):
    def __init__(self, *args, target_users=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_users = target_users

    def send(self):
        if settings.ANYMAIL.get('MAILGUN_API_KEY') and settings.DEFAULT_FROM_EMAIL:
            if self.target_users:
                email = self.message.email
                email.to = [user.email for user in self.target_users]
                email.send()
        else:
            logging.error('Notifications: Email not configured!')


class Mattermost(MessageTransport):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.url = settings.MATTERMOST_WEBHOOK_URL
        self.channel = settings.MATTERMOST_CHANNEL
        self.username = settings.MATTERMOST_USERNAME

    def send(self):
        if self.url and self.channel and self.username:
            attachments = self.message.mattermost
            response = requests.post(self.url, json={
                'username': self.username,
                'channel': self.channel,
                "attachments": attachments
            })

            if response.status_code != 200:
                try:
                    error_message = json.loads(response.text)
                except ValueError:
                    error_message = {'message': response.text, 'status_code': response.status_code}
                raise Exception(f"[Mattermost Error] Status: {error_message.get('status_code')} Message: {error_message.get('message')}")
        else:
            logging.error('Notifications: Mattermost not configured!')


class SMS(MessageTransport):
    def __init__(self, *args, target_users=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_users = target_users

    def send(self):
        if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_PHONE_NUMBER:
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

            for user in self.target_users:
                if user.settings.phone_number:
                    message = client.messages.create(
                        to=user.settings.phone_number,
                        from_=settings.TWILIO_PHONE_NUMBER,
                        body=self.message.sms)
                    logging.info(f'SMS Sent. SID: {message.sid}')
                else:
                    logging.error(f'Tried to send SMS, but no phone number set for user. user id: {user.id}')
        else:
            logging.error('SMS service not configured!')
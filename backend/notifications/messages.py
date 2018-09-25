from abc import ABCMeta, abstractmethod

from anymail.message import attach_inline_image_file
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.utils import translation

from helpers.url import get_backend_link, get_frontend_link
from helpers.messages import (
    email_html_to_text, file_to_mimeimage,
    format_default_email_images, format_details
)

class Message(metaclass=ABCMeta):
    STATUS_COLORS = {
        0: '#008000',
        1: '#FFA500',
        2: '#FF0000',
    }

    SEVERITY_COLORS = {
        0: '#B0C4DE',
        10: '#6FEB81',
        20: '#F8BC27',
        30: '#FB6613',
        40: '#FF0000'
    }

    @property
    def email(self):
        # Internationalization related to the email template
        # should be done inside the template itself!
        # See: https://docs.djangoproject.com/en/2.0/topics/i18n/translation/#internationalization-in-template-code
        metadata = format_default_email_images(self.metadata)
        self.metadata.update(metadata)
        self.metadata['details'] = format_details(
            self.metadata['details'], type='dict'
        )

        if isinstance(self.metadata['details'], (dict,)):
            self.metadata['dict_details'] = True

        subject = render_to_string(
            f'{self.templates}/email_subject.html', self.metadata
        )

        msg = EmailMultiAlternatives(
            subject=subject
        )

        logo_cid = attach_inline_image_file(
            msg, self.metadata['logo_path']
        )

        msg.mixed_subtype = 'related'

        self.metadata['logo_cid'] = logo_cid

        for icon in self.metadata['icons_data']:
            icon_name = attach_inline_image_file(
                msg, self.metadata['icons_data'][icon]
            )

            self.metadata[icon] = icon_name

        html_body = render_to_string(
            f'{self.templates}/email_body.html', self.metadata
        )
        text_body = email_html_to_text(html_body)
        msg.body = text_body
        msg.attach_alternative(html_body, 'text/html')

        return msg

    @property
    def sms(self):
        msg = self.metadata.get('subject')
        return msg

    @property
    @abstractmethod
    def mattermost(self):
        """

        :return: list that should be inserted into Mattermost transport's attachment field in payload
        """
        raise NotImplementedError('All message subclass should implement the mattermost method!')

    @property
    def metadata(self):
        """

        :return: Metadata dict generated from django models. The dict should be used by templates and other message generating methods.
        """
        return self._metadata

    @metadata.setter
    @abstractmethod
    def metadata(self, value):
        """

        :return: Metadata dict generated from django models. The dict should be used by templates.
        """
        raise NotImplementedError('All message subclass should implement the metadata setter method!')

    def __init__(self, obj, templates='notifications/event_notification/client', language='en'):
        self.obj = obj
        self.templates = templates
        self._language = language

        self._message = None
        self._metadata = {}
        self.metadata = self.obj


class EventMessage(Message):
    # noinspection PyMethodOverriding
    @Message.metadata.setter
    def metadata(self, value):
        curr_language = translation.get_language()
        translation.activate(self._language)

        self._metadata = {
            'id': value.id,
            'subject': _(value.subject),
            'details': _(value.details) if isinstance(value.details, str) else value.details,
            'status': _(value.get_status_display()),
            'severity': _(value.get_severity_display()),
            'event_type': _(value.__class__.__name__),
            # TODO: do we really need these for the templates?
            'severity_color': self.SEVERITY_COLORS[value.severity],
            'status_color': self.STATUS_COLORS[value.status],
            'language': self._language
        }

        if hasattr(value, 'file') and value.file:
            publication_code = value.file.publication.code.upper()
            file_ext = value.file.filename.split('.')[-1].upper()

            edition_date = None
            try:
                edition_date = value.file.edition.date
            except ObjectDoesNotExist:
                pass


            self.metadata['subject'] = (
                f'{publication_code}: {file_ext} | {self._metadata["subject"]}'
            )
            self.metadata['file'] = {
                'id': value.file.id,
                'filename': value.file.filename,
                'url': value.file.file,
                'edition_date': edition_date,
                'publication': {'id': value.file.publication.id, 'name': value.file.publication.name} if value.file.publication else {'id': '', 'name': ''}
            }

        if hasattr(value, 'service') and value.service:
            self.metadata['service'] = {'id': value.service.id, 'name': value.service.name}

        translation.activate(curr_language)

    @property
    def mattermost(self):
        self.metadata['details'] = format_details(
            self.metadata['details'],
            type='md'
        )

        attachment = {
            'fallback': render_to_string(f'{self.templates}/mattermost_fallback.md', self.metadata),
            'color': self.SEVERITY_COLORS[self.obj.severity],
            'text': render_to_string(f'{self.templates}/mattermost_message.md', self.metadata),
            'title': render_to_string(f'{self.templates}/mattermost_title.md', self.metadata),

            # 'title_link': 'http://docs.mattermost.com/developer/message-attachments.html',
            'fields': [
                {
                    'short': True,
                    'title': 'Server',
                    'value': f'{settings.HOSTNAME}'
                },
                {
                    'short': True,
                    'title': 'Event',
                    'value': f'{self.metadata["event_type"]} (id: {self.metadata["id"]})'
                },

                {
                    'short': True,
                    'title': 'Status',
                    'value': self.metadata['status']
                },
                {
                    'short': True,
                    'title': 'Severity',
                    'value': self.metadata['severity']
                },

            ],
        }

        if self.metadata["event_type"] == 'FileEvent':
            attachment['fields'][1] = {
                'short': True,
                'title': 'Event',
                'value': f'[FileEvent]({get_frontend_link(self.obj)}) (id: [{self.metadata["id"]}]({get_backend_link(self.obj, "admin:status_fileevent_change")}))'
            }

        if hasattr(self.obj, 'file') and self.obj.file:
            attachment['fields'].append({
                'short': True,
                'title': f'File',
                'value': f'[{self.metadata["file"]["filename"]}]({get_frontend_link(self.obj.file)}) (id: [{self.metadata["file"]["id"]}]({get_backend_link(self.obj.file, "admin:status_file_change")}))'
            })
            attachment['fields'].append({
                'short': True,
                'title': 'Publication',
                'value': f'[{self.metadata["file"]["publication"]["name"]}]({get_frontend_link(self.obj.file.publication)}) (id: [{self.metadata["file"]["publication"]["id"]}]({get_backend_link(self.obj.file.publication, "admin:portal_publication_change")}))'
            })

        if hasattr(self.obj, 'service') and self.obj.service:
            attachment['fields'].append({
                'short': True,
                'title': f'Service',
                'value': f'[{self.metadata["service"]["name"]}]({get_frontend_link(self.obj.service)}) (id: [{self.metadata["service"]["id"]}]({get_backend_link(self.obj.service, "admin:status_service_change")}))'
            })

        return [attachment]


class ScheduleMessage(Message):
    # noinspection PyMethodOverriding
    @Message.metadata.setter
    def metadata(self, value):
        curr_language = translation.get_language()
        translation.activate(self._language)
        self._metadata = {
            'id': self.obj.id,
            'name': self.obj.name,
            'subject': _('Schedule missed.'),
            'details': _('Schedule missed for publication.'),
            'publication': {'id': self.obj.publication.id, 'name': self.obj.publication.name} if self.obj.publication else {'id': '', 'name': ''},
            'language': self._language
        }
        translation.activate(curr_language)

    @property
    def mattermost(self):
        self.metadata['details'] = format_details(
            self.metadata['details'],
            type='md'
        )
        attachment = {
            'fallback': render_to_string(f'{self.templates}/mattermost_fallback.md', self.metadata),
            'color': '#FB6613',
            'text': render_to_string(f'{self.templates}/mattermost_message.md', self.metadata),
            'title': render_to_string(f'{self.templates}/mattermost_title.md', self.metadata),

            # 'title_link': 'http://docs.mattermost.com/developer/message-attachments.html',
            'fields': [
                {
                    'short': True,
                    'title': 'Server',
                    'value': f'{settings.HOSTNAME}'
                },
                {
                    'short': True,
                    'title': 'Schedule',
                    'value': f'Schedule (id: {self.metadata["id"]}) {self.metadata["name"]}'
                },
                {
                    'short': True,
                    'title': 'Publication',
                    'value': f'[{self.metadata["publication"]["name"]}]({get_frontend_link(self.obj.publication)}) (id: [{self.metadata["publication"]["id"]}]({get_backend_link(self.obj.publication, "admin:portal_publication_change")}))'
                },
            ],
        }

        return [attachment]

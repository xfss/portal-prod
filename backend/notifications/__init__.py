from abc import ABCMeta, abstractmethod
from typing import Iterable

from django.contrib.auth import get_user_model
from django.db.models import Q

from helpers.language import get_publication_lang
from notifications.messages import EventMessage, ScheduleMessage
from notifications.transports import Email, Mattermost, SMS

from portal.models import Publication

User = get_user_model()


class NotificationBase(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        self.transporters = []

    def send(self):
        for transporter in self.transporters:
            transporter.send()

    @staticmethod
    def _get_users_for_transports(publications: Iterable[Publication], channel: int, severity: int = None, status: int = None):
        from status.models import NotificationSubscription

        users = {'email': [], 'sms': []}

        query = Q(event_channel=channel) & Q(user__membership__publication__in=publications)
        if severity is not None:
            query &= (Q(severity__isnull=True) | Q(severity__lte=severity))
        if status is not None:
            query &= (Q(status__isnull=True) | Q(status=status))

        for subscription in NotificationSubscription.objects.select_related('user').filter(query):
            users[subscription.get_notification_type_display().lower()].append(subscription.user)
        return users


class EventNotification(NotificationBase):
    def __init__(self, event):
        # Import these here to avoid circular import
        from status.models import EventSeverity, FileEvent, Notification, ServiceEvent, ScheduleEvent

        super().__init__()

        publications = []
        if isinstance(event, FileEvent) and event.file.publication:
            publications = [event.file.publication]
            publication_language = get_publication_lang(event.file.publication)
        elif isinstance(event, ServiceEvent) and event.service.publication:
            publications = event.service.publication.all()
            if len(publications) == 1:
                publication_language = get_publication_lang(publications[0])
            else:
                publication_language = get_publication_lang(None)
        elif isinstance(event, Notification):
            publications = [event.publication]
            publication_language = get_publication_lang(None)
        else:
            # Fallback if the event is not the expected type. This should never happen.
            publication_language = get_publication_lang(None)


        if isinstance(event, ScheduleEvent):
            operations_message = ScheduleMessage(obj=event.schedule, templates='notifications/schedule_notification/operations')
            client_message = ScheduleMessage(obj=event.schedule, templates='notifications/schedule_notification/client', language=get_publication_lang(event.schedule.publication))
            users = self._get_users_for_transports((event.schedule.publication,), event.channel)
        else:
            operations_message = EventMessage(
                event,
                'notifications/event_notification/operations'
            )

            client_message = EventMessage(
                event,
                'notifications/event_notification/client',
                language=publication_language
            )
            users = self._get_users_for_transports(publications, event.channel, event.severity, event.status)

        # Send everything to mattermost for now
        if event.severity >= EventSeverity.INFO:
            self.transporters.append(Mattermost(message=operations_message))

        self.transporters.append(Email(message=client_message, target_users=users['email']))
        self.transporters.append(SMS(message=client_message, target_users=users['sms']))

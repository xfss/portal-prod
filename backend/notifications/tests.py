import pendulum
import pytest
from django.contrib.auth import get_user_model

from notifications import EventNotification, Email, ScheduleMessage, Mattermost
from portal.models import Publication, Membership
from status.models import NotificationSubscription, EventChannel, NotificationType, EventSeverity, EventStatus, FileEvent, File, Schedule, ScheduleEvent, Edition

User = get_user_model()


@pytest.mark.django_db
def test_notification_channels():
    # Setup
    user1 = User(username='a', password='aa')
    user1.save()
    user2 = User(username='b', password='bb')
    user2.save()
    user3 = User(username='c', password='cc')
    user3.save()
    user4 = User(username='d', password='dd')
    user4.save()

    dummy_publication = Publication(name='Dummy publication', code='DUMMY')
    dummy_publication.save()

    membership = Membership(user=user1, publication=dummy_publication, role=Membership.ADMIN)
    membership.save()
    membership = Membership(user=user2, publication=dummy_publication, role=Membership.ADMIN)
    membership.save()
    membership = Membership(user=user3, publication=dummy_publication, role=Membership.ADMIN)
    membership.save()

    dummy_file = File(filename='20180101_dummy.pdf', category=File.EDITION, publication=dummy_publication)
    dummy_file.save()

    # Add different channel subscriptions
    notification_subscription = NotificationSubscription(user=user1, event_channel=EventChannel.FILE_UPLOAD, notification_type=NotificationType.EMAIL, severity=None, status=None)
    notification_subscription.save()
    notification_subscription = NotificationSubscription(user=user1, event_channel=EventChannel.SCHEDULE_MISSED, notification_type=NotificationType.EMAIL, severity=None, status=None)
    notification_subscription.save()
    notification_subscription = NotificationSubscription(user=user2, event_channel=EventChannel.FILE_UPLOAD, notification_type=NotificationType.EMAIL, severity=EventSeverity.LOW, status=None)
    notification_subscription.save()
    notification_subscription = NotificationSubscription(user=user2, event_channel=EventChannel.SCHEDULE_MISSED, notification_type=NotificationType.EMAIL, severity=EventSeverity.LOW, status=None)
    notification_subscription.save()
    notification_subscription = NotificationSubscription(user=user3, event_channel=EventChannel.FILE_UPLOAD, notification_type=NotificationType.EMAIL, severity=EventSeverity.MEDIUM,
                                                         status=EventStatus.ERROR)
    notification_subscription.save()
    notification_subscription = NotificationSubscription(user=user3, event_channel=EventChannel.SCHEDULE_MISSED, notification_type=NotificationType.EMAIL, severity=None, status=None)
    notification_subscription.save()
    notification_subscription = NotificationSubscription(user=user4, event_channel=EventChannel.FILE_UPLOAD, notification_type=NotificationType.EMAIL, severity=None, status=None)
    notification_subscription.save()
    notification_subscription = NotificationSubscription(user=user4, event_channel=EventChannel.SCHEDULE_MISSED, notification_type=NotificationType.EMAIL, severity=None, status=None)
    notification_subscription.save()

    # Check if we get the expected users based on subscriptions
    event = FileEvent(file=dummy_file, severity=EventSeverity.MEDIUM, status=EventStatus.ERROR, channel=EventChannel.FILE_UPLOAD)
    event.save()
    notification = EventNotification(event)
    for transporter in notification.transporters:
        if isinstance(transporter, Email):
            assert [user1, user2, user3] == transporter.target_users
            break
    else:
        raise Exception('No email transport found!')

    event = FileEvent(file=dummy_file, severity=EventSeverity.LOW, status=EventStatus.ERROR, channel=EventChannel.FILE_UPLOAD)
    event.save()
    notification = EventNotification(event)
    for transporter in notification.transporters:
        if isinstance(transporter, Email):
            assert [user1, user2] == transporter.target_users
            break
    else:
        raise Exception('No email transport found!')

    event = FileEvent(file=dummy_file, severity=EventSeverity.MEDIUM, status=EventStatus.SUCCESS, channel=EventChannel.FILE_UPLOAD)
    event.save()
    notification = EventNotification(event)
    for transporter in notification.transporters:
        if isinstance(transporter, Email):
            assert [user1, user2] == transporter.target_users
            break
    else:
        raise Exception('No email transport found!')

    # Schedule notification does not have a severity or status for now so every subscribed user should be notified
    schedule = Schedule(name='test schedule', publication=dummy_publication)
    schedule.save()
    edition = Edition(date=pendulum.today())
    edition.save()

    event = ScheduleEvent(schedule=schedule, edition=edition, severity=EventSeverity.HIGH, status=EventStatus.ERROR, channel=EventChannel.SCHEDULE_MISSED)
    event.save()

    notification = EventNotification(event)
    email_found = False
    mattermost_found = False
    for transporter in notification.transporters:
        if isinstance(transporter, Email):
            assert [user1, user2, user3] == transporter.target_users
            assert isinstance(transporter.message, ScheduleMessage)
            assert transporter.message.templates == 'notifications/schedule_notification/client'
            email_found = True
        if isinstance(transporter, Mattermost):
            assert isinstance(transporter.message, ScheduleMessage)
            assert transporter.message.templates == 'notifications/schedule_notification/operations'
            mattermost_found = True

    assert email_found
    assert mattermost_found

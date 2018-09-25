from datetime import datetime

import re
import pendulum
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils.translation import gettext_noop as _
from dry_rest_permissions.generics import allow_staff_or_superuser
from recurrence.fields import RecurrenceField

from portal.models import Publication, Membership
from notifications import EventNotification

User = get_user_model()


class EventStatus:
    """

    Status choices for Event models.

    """
    SUCCESS = 0
    IN_PROGRESS = 1
    ERROR = 2

    # For Django choice fields
    CHOICES = (
        (SUCCESS, _('Success')),
        (IN_PROGRESS, _('In progress')),
        (ERROR, _('Error')),
    )


class EventSeverity:
    """

    Severity choices for Event models.

    """

    # The gap in between severity int is to make it possible to add new severity levels in between in the future more easily.
    INFO = 0
    LOW = 10
    MEDIUM = 20
    HIGH = 30
    CRITICAL = 40

    # For Django choice fields
    CHOICES = (
        (INFO, _('Info')),
        (LOW, _('Low')),
        (MEDIUM, _('Medium')),
        (HIGH, _('High')),
        (CRITICAL, _('Critical')),
    )


class EventChannel:
    """

    Type choices for Event models.

    """

    FILE_UPLOAD = 0
    FILE_PROCESSING = 1
    USER_INPUT_NEEDED = 2
    PUBLICATION = 3
    SCHEDULE_MISSED = 4

    CHOICES = (
        (FILE_UPLOAD, _('File Upload')),
        (FILE_PROCESSING, _('File Processing')),
        (USER_INPUT_NEEDED, _('User input needed')),
        (PUBLICATION, _('Edition published')),
        (SCHEDULE_MISSED, _('Schedule missed')),
    )


class NotificationType:
    """

    Notification type choices for Events models.

    """

    EMAIL = 0
    SMS = 1

    CHOICES = (
        (EMAIL, _('Email')),
        (SMS, _('SMS')),
    )


class EventBase(models.Model):
    """

    Base class for event models. All event like model should inherit from this abstract class.

    """
    subject = models.CharField(max_length=200)
    details = models.TextField()
    timestamp = models.DateTimeField(editable=False, auto_now_add=True)

    status = models.IntegerField(choices=EventStatus.CHOICES)
    severity = models.IntegerField(choices=EventSeverity.CHOICES)

    channel = models.IntegerField(choices=EventChannel.CHOICES, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ('-timestamp',)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        notification = EventNotification(self)
        notification.send()


class Service(models.Model):
    name = models.CharField(max_length=50)
    friendly_name = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200)  # or url?
    port = models.IntegerField(blank=True, null=True)
    parameters = JSONField(blank=True, default={})
    secure_parameters = JSONField(blank=True, default={})
    filename_pattern = models.CharField(max_length=500, null=True)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=True, auto_now_add=True)
    creator = models.ForeignKey(to=User, related_name='%(class)s_creator', null=True, on_delete=models.SET_NULL)
    updater = models.ForeignKey(to=User, related_name='%(class)s_updater', null=True, on_delete=models.SET_NULL)
    publication = models.ManyToManyField(Publication, blank=True, through='PublicationService', through_fields=('service', 'publication'))

    # Type field
    SFTP = 1
    ABODB = 2
    PAPERLIT = 3
    TYPE_CHOICES = (
        (SFTP, _('SFTP')),
        (ABODB, _('AboDB')),
        (PAPERLIT, _('Paperlit')),
    )
    type = models.IntegerField(choices=TYPE_CHOICES)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'Service: {self.name} (id: {self.id})'

    def save(self, *args, **kwargs):
        new = not self.id
        super().save(*args, **kwargs)

        if new:
            service_event = ServiceEvent(
                service=self,
                subject=_('Service Created'),
                details=_('Service created successfully.'),
                timestamp=datetime.now(),
                status=EventStatus.SUCCESS,
                severity=EventSeverity.INFO,
                originator_user=self.creator
            )
        else:
            service_event = ServiceEvent(
                service=self,
                subject=_('Service Updated'),
                details=_('Service updated successfully.'),
                timestamp=datetime.now(),
                status=EventStatus.SUCCESS,
                severity=EventSeverity.INFO,
                originator_user=self.creator
            )
            service_event.save()

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return self.publication and self.publication.membership_set.filter(user=request.user).count() > 0

    @allow_staff_or_superuser
    def has_object_write_permission(self):
        # Service should be only editable by staff for now
        return False

    @staticmethod
    def has_create_permission(request):
        return True


class PublicationService(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    release_offset_time = models.DurationField(blank=True, default=0)

    class Meta:
        unique_together = ('publication', 'service')


class ServiceEvent(EventBase):
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)
    originator_user = models.ForeignKey(
        to=User,
        related_name='%(class)s_originator_user',
        null=True,
        on_delete=models.SET_NULL
    )

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return self.service and self.service.publication and self.service.publication.filter(membership__user=request.user).count() > 0

    def has_object_write_permission(self):
        return False

    @staticmethod
    def has_create_permission(request):
        return False


class File(models.Model):
    # This is the original/desired filename. Kept in case of name collision.
    filename = models.CharField(max_length=200, blank=True)
    file = models.FileField(
        validators=[
            FileExtensionValidator(allowed_extensions=['pdf', 'csv'])
        ]
    )
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=True, auto_now_add=True)
    creator = models.ForeignKey(to=User, related_name='%(class)s_creator', null=True, on_delete=models.SET_NULL)
    updater = models.ForeignKey(to=User, related_name='%(class)s_updater', null=True, on_delete=models.SET_NULL)
    publication = models.ForeignKey(to=Publication, null=True, on_delete=models.SET_NULL)

    EDITION = 0
    SUBSCRIPTIONS = 1

    # For Django choice fields
    CATEGORY_CHOICES = (
        (EDITION, _('Edition')),
        (SUBSCRIPTIONS, _('Subscriptions')),
    )
    category = models.IntegerField(choices=CATEGORY_CHOICES, null=False, blank=True)

    class Meta:
        ordering = ('-edition__date', '-updated_at', '-created_at')

    def __str__(self):
        return f'File: {self.filename} (id: {self.id})'

    def save(self, *args, **kwargs):
        if not self.filename and self.file:
            self.filename = self.file.name

            if not self.category:
                file_ext = self.filename.split('.')[-1].lower()
                if file_ext == 'pdf':
                    self.category = File.EDITION
                elif file_ext == 'csv':
                    self.category = File.SUBSCRIPTIONS
                else:
                    raise Exception('Wrong file type.')

            # In case of no publication set already (from frontend input or from serializer) try to match filename based on pattern
            if not self.publication:
                found = False
                publications = Publication.objects.exclude(filename_pattern='').exclude(filename_pattern=None)
                for publication in publications:
                    pattern = re.compile(publication.filename_pattern, re.IGNORECASE)

                    if pattern.match(self.filename):
                        self.publication = publication
                        if found:
                            # TODO: Handle this more gracefully in the future
                            raise Exception('Filename matched to more than one publisher!')
                        else:
                            found = True

        super().save(*args, **kwargs)

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return self.publication and self.publication.membership_set.filter(user=request.user).count() > 0

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return self.publication and self.publication.membership_set.filter(user=request.user, role__in=[Membership.ADMIN]).count() > 0

    @staticmethod
    def has_create_permission(request):
        return True


class FileEvent(EventBase):
    file = models.ForeignKey(File, null=True, on_delete=models.SET_NULL)
    service = models.ForeignKey(Service, null=True, on_delete=models.SET_NULL)

    originator_user = models.ForeignKey(
        to=User,
        related_name='%(class)s_originator_user',
        null=True,
        on_delete=models.SET_NULL
    )
    originator_service = models.ForeignKey(
        to=Service,
        related_name='%(class)s_originator_service',
        null=True,
        on_delete=models.SET_NULL
    )

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return self.file and self.file.publication and self.file.publication.membership_set.filter(user=request.user).count() > 0

    def has_object_write_permission(self):
        return False

    @staticmethod
    def has_create_permission(request):
        return False


class Edition(models.Model):
    publication = models.ForeignKey(to=Publication, null=True, on_delete=models.SET_NULL)
    file = models.OneToOneField(File, null=True, on_delete=models.CASCADE)
    date = models.DateField(null=True)

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=True, auto_now_add=True)

    class Meta:
        unique_together = (('publication', 'date'),)


class Notification(EventBase):
    """Use for single notifications not attached to files."""
    publication = models.ForeignKey(
        Publication,
        null=True,
        on_delete=models.SET_NULL
    )
    subject = models.CharField(max_length=160, default='', null=True)
    details = models.TextField(max_length=160, default='', null=True)

    def clean(self, *args, **kwargs):
        """
        Validate fields.

        `publication` is allowed to be null so that if the
        referenced field is ever deleted, we don't remove the
        notifications from the DB.
        In spite of the above, notifications need a `publication`
        in order to be sent.
        """
        super().clean(*args, **kwargs)
        if not self.publication:
            raise ValidationError(
                _('Cannot save object without a "Publication".'),
                code='required'
            )

    def __str__(self):
        return self.publication.code


class Schedule(models.Model):
    name = models.CharField(max_length=50)
    recurrence = RecurrenceField()
    publication = models.ForeignKey(to=Publication, on_delete=models.CASCADE)

    class Meta:
        ordering = ('name',)

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return self.publication and self.publication.membership_set.filter(user=request.user).count() > 0

    @allow_staff_or_superuser
    def has_object_write_permission(self):
        return False

    @allow_staff_or_superuser
    def has_create_permission(self, request):
        return False


class ScheduleEvent(EventBase):
    schedule = models.ForeignKey(Schedule, null=False, on_delete=models.CASCADE)
    edition = models.ForeignKey(Edition, null=True, on_delete=models.SET_NULL)

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return self.schedule.publication and self.schedule.publication.membership_set.filter(user=request.user).count() > 0

    def has_object_write_permission(self):
        return False

    @staticmethod
    def has_create_permission(request):
        return False


class NotificationSubscription(models.Model):
    user = models.ForeignKey(
        User,
        related_name='notification_subscriptions',
        on_delete=models.CASCADE
    )
    event_channel = models.IntegerField(choices=EventChannel.CHOICES)
    notification_type = models.IntegerField(
        choices=NotificationType.CHOICES,
        help_text='How to send the notification out.'
    )

    status = models.IntegerField(
        choices=EventStatus.CHOICES,
        null=True,
        blank=True,
        help_text=('Notify about status level equal to this level. '
                   'Blank sends out notification regardless of status level.')
    )
    severity = models.IntegerField(
        choices=EventSeverity.CHOICES,
        null=True,
        blank=True,
        help_text=('Notify about severity level equal or higher than this. '
                   'Blank sends out notification regardless '
                   'of severity level.')
    )

    # TODO: Implement per publication subscriptions if we need them
    # In case of publication=None it will be considered as a global subscription
    # publication = models.ForeignKey(Publication, null=True, blank=True, on_delete=models.CASCADE)

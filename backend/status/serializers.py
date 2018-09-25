import json
import re
import os.path as os_path
from datetime import datetime

import pendulum
from django.utils import timezone
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from fields.language import LocalizedDateTimeField, LocalizedDateField
from portal.models import Publication
from portal.serializers import UserBriefSerializer, PublicationBriefSerializer
from status.models import (
    EventChannel, EventSeverity, EventStatus, File,
    FileEvent, Notification, Schedule, Service, ServiceEvent,
    Edition)


class TranslatedModelSerializerBase(serializers.ModelSerializer):
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return {k: _(v) if isinstance(v, str) else v for k, v in ret.items()}


class EventSerializerBase(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=EventStatus.CHOICES, source='get_status_display', read_only=True)
    severity = serializers.ChoiceField(choices=EventSeverity.CHOICES, source='get_severity_display', read_only=True)
    channel = serializers.ChoiceField(choices=EventChannel.CHOICES, source='get_channel_display', read_only=True)
    timestamp = LocalizedDateTimeField(read_only=True)


class ServiceSerializer(TranslatedModelSerializerBase):
    status = serializers.SerializerMethodField()
    publication = PublicationBriefSerializer(many=True, read_only=True)

    created_at = LocalizedDateTimeField(read_only=True)
    updated_at = LocalizedDateTimeField(read_only=True)

    creator = UserBriefSerializer(many=False, read_only=True)
    updater = UserBriefSerializer(many=False, read_only=True)

    class Meta:
        model = Service
        fields = '__all__'
        extra_kwargs = {
            'secure_parameters': {'write_only': True}
        }

    @staticmethod
    def get_status(obj):
        events = ServiceEvent.objects.order_by('-timestamp', ).filter(service=obj)
        if events:
            return events[0].get_status_display()


class ServiceEventSerializer(TranslatedModelSerializerBase, EventSerializerBase):
    service = ServiceSerializer(many=False, read_only=True)

    class Meta:
        model = ServiceEvent
        fields = '__all__'


class EditionSerializer(TranslatedModelSerializerBase):
    date = LocalizedDateField(read_only=True)
    created_at = LocalizedDateTimeField(read_only=True)
    updated_at = LocalizedDateTimeField(read_only=True)

    class Meta:
        model = Edition
        fields = ('id', 'date', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class FileSerializer(TranslatedModelSerializerBase):
    status = serializers.SerializerMethodField()
    detailed_status = serializers.SerializerMethodField()
    publication = PublicationBriefSerializer(many=False, read_only=True)
    event_number = serializers.SerializerMethodField()
    created_at = LocalizedDateTimeField(read_only=True)
    updated_at = LocalizedDateTimeField(read_only=True)
    edition = EditionSerializer(required=False)
    category = serializers.ChoiceField(choices=File.CATEGORY_CHOICES, source='get_category_display', required=False)

    creator = UserBriefSerializer(many=False, read_only=True)
    updater = UserBriefSerializer(many=False, read_only=True)

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ('file_name',)

    @staticmethod
    def get_status(obj):
        events = FileEvent.objects.order_by('-timestamp', ).filter(file=obj)
        if events:
            return events[0].get_status_display()
        else:
            return 'Success'

    @staticmethod
    def get_detailed_status(obj):
        events = FileEvent.objects.filter(file=obj).order_by('service__id', '-timestamp').distinct('service__id')
        if events:
            detailed_statuses = {event.service.name: event.get_status_display() for event in events if event.service}

            priority_events = FileEvent.objects.filter(file=obj, severity__gte=EventSeverity.MEDIUM).order_by('service_id', '-timestamp').distinct('service__id')
            if priority_events:
                detailed__priority_statuses = {event.service.name: event.get_status_display() for event in priority_events if event.service}
                return {**detailed_statuses, **detailed__priority_statuses}
            else:
                return detailed_statuses
        else:
            return {}

    @staticmethod
    def get_event_number(obj):
        return FileEvent.objects.filter(file=obj).count()

    def to_internal_value(self, data):
        publication_id = data.get('publication', None)
        result = super().to_internal_value({k: v for k, v in data.items() if k != 'publication'})

        if publication_id:
            publication_id = int(publication_id[0])
            result['publication'] = publication_id
        return result

    def create(self, validated_data):
        publication_id = validated_data.pop('publication', None)
        file = File(**validated_data)
        if publication_id:
            publication = Publication.objects.get(id=publication_id)
            if publication:
                if file.creator.is_staff or publication.membership_set.filter(user=file.creator).count() > 0:
                    file.publication = publication
                else:
                    raise PermissionDenied(f'{_("File upload: User has no rights to publication")}: {publication.name}')
            else:
                raise Exception('Invalid publication id while saving file!')
        else:
            # Automatically add publication to file if user has only one publication and he did not tried to set it to anything
            publications = Publication.objects.filter(membership__user=file.creator)
            if len(publications) == 1:
                file.publication = publications[0]

        self.validate_filename_on_create(file)

        file.save()

        self.check_edition_schedule(file)

        return file

    def validate_filename_on_create(self, file):
        """Validate file name and notify publication uploader on error."""
        publication_code = None
        publication = file.publication
        publications = []

        name, ext = os_path.splitext(file.file.name)

        # Only validate Editions (pdf)
        if re.match('(?:\.)?pdf', ext, re.IGNORECASE):
            validation_error = False
            publication = None
            edition_date = None

            # Check for date and publication code
            pattern = re.match(
                '^(?P<date>\d{8})\_(?P<code>\w{2,3})(?:\_)?', name
            )
            if not pattern:
                validation_error = 1
            else:
                filename_date = pattern.group('date')
                edition_date = pendulum.parse(filename_date)
                if edition_date.date() < timezone.now().date():
                    validation_error = 2

                if not publication and 'code' in pattern.groupdict():
                    publication_code = pattern.group('code')

            if validation_error:
                error = 'File name validation error'

                if validation_error == 1:
                    error = _('The file name for uploaded file '
                              f'"{file.file.name}" does not match the '
                              'expected file name pattern.')
                elif validation_error == 2:
                    error = _('Edition date for uploaded file '
                              f'"{file.file.name}" cannot be in the past.')

                if publication_code and not publication:
                    try:
                        publication = Publication.objects.get(
                            code=publication_code)
                    except Publication.DoesNotExist:
                        pass

                if not publication:
                    publications = Publication.objects.filter(
                        members=file.creator
                    )

                    pub = None
                    # Match file name again without checking date
                    pattern = re.search(
                        '(?:\_)(?P<code>[a-zA-Z]{2,3})(?:\_)?',
                        name,
                        re.IGNORECASE
                    )
                    if pattern and 'code' in pattern.groupdict():
                        for pub in publications:
                            if pub.code == pattern.groupdict()['code']:
                                publication = pub
                                break

                if not publication and publications:
                    publication = publications[0]

                if publication:
                    details = {
                        _('Error'): error,
                        _('File'): file.file.name,
                    }

                    if edition_date:
                        details[_('Edition date')] = str(edition_date.date())

                    self.notify_validation(
                        publication, error, EventStatus.ERROR,
                        EventSeverity.HIGH, **details
                    )

                raise serializers.ValidationError(error)

    def check_edition_schedule(self, file):
        """Check uploaded file with Publication schedule."""
        publication = file.publication
        now = datetime.now()

        for s in Schedule.objects.filter(publication=publication):
            edition_dt = datetime(file.edition.date.year, file.edition.date.month, file.edition.date.day)

            # Check if edition date matches this schedule:
            if len(s.recurrence.between(edition_dt, datetime(file.edition.date.year, file.edition.date.month, file.edition.date.day + 1))) == 1:
                # This intentionally not include the date for the edition like the check before this, so we can know the number of editions between the file's and now
                editions_from_now = len(s.recurrence.between(now, edition_dt))
                if publication.configuration.get('advance_edition_max', 1) < editions_from_now:
                    message = _(
                        'The Edition date for the uploaded file '
                        f'"{file.file.name}" is for {(edition_dt - now).days} days from now. There is {editions_from_now - 1} editions before this one.'
                    )
                    self.notify_validation(
                        publication, message,
                        EventStatus.ERROR, EventSeverity.MEDIUM
                    )
                break
        else:
            # File edition did not matched any schedule
            message = _(
                ('The Edition day for the uploaded file '
                 f'"{file.file.name}" does not match the usual '
                 f'schedule for "{publication.name}"')
            )
            self.notify_validation(
                publication, message,
                EventStatus.ERROR, EventSeverity.MEDIUM
            )

    def notify_validation(self, publication, message,
                          status, severity, **details):
        event_data = {
            'status': status,
            'severity': severity,
            'subject': message,
            'details': json.dumps(details),
            'publication': publication,
            'channel': EventChannel.FILE_UPLOAD
        }

        notification = Notification(**event_data)
        notification.save()


class FileEventSerializer(TranslatedModelSerializerBase, EventSerializerBase):
    file = FileSerializer(many=False, read_only=True)
    originator_user = UserBriefSerializer(many=False, read_only=True)

    class Meta:
        model = FileEvent
        fields = '__all__'

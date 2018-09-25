import coreapi
import coreschema
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from dry_rest_permissions.generics import DRYObjectPermissions
from rest_framework.schemas import ManualSchema

from helpers.schema import get_inequality_schema_fields
from status.models import File, FileEvent, Service, ServiceEvent
from status.serializers import (
    ServiceSerializer, ServiceEventSerializer, FileSerializer,
    FileEventSerializer
)

User = get_user_model()


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = (IsAuthenticated, DRYObjectPermissions,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updater=self.request.user)


class ServiceEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceEvent.objects.all()
    serializer_class = ServiceEventSerializer
    permission_classes = (IsAuthenticated, DRYObjectPermissions,)

    def perform_create(self, serializer):
        serializer.save(originator_user=self.request.user)


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated, DRYObjectPermissions,)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updater=self.request.user)

    @detail_route(
        methods=('get',),
        schema=ManualSchema(
            fields=[
                coreapi.Field('id', required=True, location="path", schema=coreschema.Integer()),
                coreapi.Field('channel', required=False, location="query", schema=coreschema.Integer(description='Filter returned events by notification channel.')),
                coreapi.Field('channel__in', required=False, location="query", schema=coreschema.Array(description='Filter returned events by notification channels in this comma separated list. (or array in coreapi.js params)')),
            ] +
            get_inequality_schema_fields('status', description='Filter returned events by status', location='query', required=False, schema=coreschema.Integer) +
            get_inequality_schema_fields('severity', description='Filter returned events by severity', location='query', required=False, schema=coreschema.Integer)
        ),
    )
    def events(self, request, pk=None):
        extra_filters = {}
        for param, value in request.query_params.items():
            # These choice fields are integer so value should be converted to int
            if any((i in param for i in ['status', 'severity'])):
                value = int(value)

            if param == 'channel__in':
                value = value.split(',')
            extra_filters[param] = value

        file = self.get_object()

        if not request.user.is_staff:
            user_memberships = file.publication.membership_set.filter(user=request.user)
            notification_channels = tuple(subscription.event_channel for subscription in request.user.notificationsubscription_set.all())

            # TODO: Add extra filters based on membership roles and notification channels!
            auth_filters = {}

        file_events = FileEvent.objects.filter(file=file, **extra_filters)
        if not file_events.exists():
            return Response({
                'status': _('Not found'),
                'message': f'{_("No file event found for file with id:")} {pk}'
            })
        serializer = FileEventSerializer(file_events, many=True, context={'request': self.request})
        return Response(serializer.data)


class FileEventViewSet(viewsets.ModelViewSet):
    queryset = FileEvent.objects.all()
    serializer_class = FileEventSerializer
    permission_classes = (IsAuthenticated, DRYObjectPermissions,)

    def perform_create(self, serializer):
        serializer.save(originator_user=self.request.user)

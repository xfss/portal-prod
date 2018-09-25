import coreapi
import coreschema
from rest_framework.permissions import IsAuthenticated
from dry_rest_permissions.generics import DRYObjectPermissions
from rest_framework.schemas import AutoSchema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.exceptions import ValidationError
from helpers.model import find_choice_by_name
from status.models import File, Service, FileEvent, EventStatus, EventSeverity


class WebhookFileEventView(APIView):
    queryset = FileEvent.objects.all()
    permission_classes = (IsAuthenticated, DRYObjectPermissions,)

    schema = AutoSchema(
        manual_fields=[
            coreapi.Field('file', required=True, location="body", schema=coreschema.String(description='File name for file event. This will be used to reverse look up the file model instance.')),
            coreapi.Field('service', required=True, location="body", schema=coreschema.Integer(description='Service id for file event. Needet to bind the event to a service.')),
            coreapi.Field('status', required=True, location="body", schema=coreschema.String(description=f"Status name or id. Possible values: {', '.join([f'{n} ({i})' for i, n in EventStatus.CHOICES])}")),
            coreapi.Field('severity', required=True, location="body", schema=coreschema.String(description=f"Severity name or id. Possible values: {', '.join([f'{n} ({i})' for i, n in EventSeverity.CHOICES])}")),
        ]
    )

    def post(self, request, format=None):
        file = request.data.get('file')
        service = request.data.get('service')
        if file and service:
            files = File.objects.filter(filename__iexact=file).order_by('-created_at')
            # TODO: look up service based on api key, when api key based access gets implemented for services
            service_obj = Service.objects.get(id=service)
            status = find_choice_by_name(choices=EventStatus.CHOICES, value=request.data.get('status', EventStatus.SUCCESS))
            severity = find_choice_by_name(choices=EventSeverity.CHOICES, value=request.data.get('severity', EventSeverity.INFO))

            if files.exists() and service:
                file_event = FileEvent(
                    file=files.first(),
                    service=service_obj,
                    subject=request.data.get('subject', ''),
                    details=request.data.get('details', ''),
                    channel=request.data.get('channel'),
                    status=status,
                    severity=severity
                )
                file_event.save()
                return Response(status=HTTP_201_CREATED,)
            return Response(status=HTTP_404_NOT_FOUND)
        else:
            raise ValidationError({"Error": "File and service fields are mandatory!"})

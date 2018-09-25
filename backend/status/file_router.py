import re
from io import StringIO
from datetime import timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_noop as _

from services.abodb import upload_abodb_csv
from services.paperlit import upload_paperlit_pdf
from status.models import Service, FileEvent, EventStatus, EventSeverity, PublicationService
from services.sftp import upload_to_sftp
from paramiko import RSAKey


def route_file(model_instance):
    for service in Service.objects.all():
        if service.filename_pattern:
            pattern = re.compile(service.filename_pattern, re.IGNORECASE)
            if pattern.match(model_instance.filename) and PublicationService.objects.filter(publication=model_instance.publication, service=service):
                event_start = FileEvent(
                    file=model_instance,
                    service=service,
                    subject=_('File name pattern match.'),
                    details=_('File name pattern match. Service handler started.'),
                    status=EventStatus.SUCCESS,
                    severity=EventSeverity.INFO,
                    originator_user=model_instance.updater or model_instance.creator
                )
                event_start.save()

                try:
                    publication_service = model_instance.publication.publicationservice_set.get(service=service).release_offset_time
                    offset = publication_service
                except ObjectDoesNotExist:
                    offset = timedelta()

                result = None
                if service.type == Service.SFTP:
                    event_file_upload = FileEvent(
                        file=model_instance,
                        service=service,
                        subject=_('Service call start.'),
                        details=_('File upload to sftp started.'),
                        status=EventStatus.SUCCESS,
                        severity=EventSeverity.INFO,
                        originator_user=model_instance.updater or model_instance.creator
                    )
                    event_file_upload.save()

                    private_key = RSAKey.from_private_key(StringIO(service.secure_parameters.get('private_key')))

                    # TODO: Check if all service parameter are present and create service error event if any of them missing.
                    result = upload_to_sftp(
                        file_object=model_instance.file,
                        filename=model_instance.filename,
                        host=service.address,
                        port=service.port or 80,
                        directory=service.parameters.get('target_directory'),
                        create_sub=service.parameters.get('create_subdirectory', False),
                        login=service.secure_parameters.get('username'),
                        private_key=private_key
                    )

                elif service.type == Service.ABODB:
                    if not model_instance.publication:
                        no_pub_event = FileEvent(
                            file=model_instance,
                            subject=_("File has no publication."),
                            details=_("File has no publication. Can't push to AboDB because of this."),
                            status=EventStatus.ERROR,
                            severity=EventSeverity.HIGH,
                            originator_user=model_instance.updater or model_instance.creator
                        )
                        no_pub_event.save()
                        continue
                    elif not model_instance.publication.code:
                        no_pub_code_event = FileEvent(
                            file=model_instance,
                            subject=_("File's publication has no code."),
                            details=_("File's publication has no code. Can't push to AboDB because of this."),
                            status=EventStatus.ERROR,
                            severity=EventSeverity.CRITICAL,
                            originator_user=model_instance.updater or model_instance.creator
                        )
                        no_pub_code_event.save()
                        continue

                    event_file_upload = FileEvent(
                        file=model_instance,
                        service=service,
                        subject=_('Service call start.'),
                        details=_('File upload to Abo DB started.'),
                        status=EventStatus.SUCCESS,
                        severity=EventSeverity.INFO,
                        originator_user=model_instance.updater or model_instance.creator
                    )
                    event_file_upload.save()

                    result = upload_abodb_csv(
                        file_object=model_instance.file,
                        abodb_url=service.address,
                        api_key=service.secure_parameters.get('api_key'),
                        publisher_code=model_instance.publication.code,
                    )
                elif service.type == Service.PAPERLIT:
                    event_file_upload = FileEvent(
                        file=model_instance,
                        service=service,
                        subject=_('Service call start.'),
                        details=_('File upload to Paperlit started.'),
                        status=EventStatus.SUCCESS,
                        severity=EventSeverity.INFO,
                        originator_user=model_instance.updater or model_instance.creator
                    )
                    event_file_upload.save()

                    result = upload_paperlit_pdf(
                        paperlit_api_url=service.address,
                        file_url=model_instance.file.url,
                        original_filename=model_instance.filename,
                        api_email=service.secure_parameters.get('api_email'),
                        api_password=service.secure_parameters.get('api_password'),
                        api_company=service.secure_parameters.get('api_company'),
                        project_id=service.parameters.get('project_id'),
                        publication_id=service.parameters.get('publication_id'),
                        publish_offset=offset,
                        default_paid=service.parameters.get('default_paid'),
                    )

                if result is not None:
                    if not result:
                        result_subject = _('Service call success.')
                        result_msg = result
                        result_status = EventStatus.SUCCESS
                        result_severity = EventSeverity.INFO
                    else:
                        result_subject = _('Service call error.')
                        result_msg = result
                        result_status = EventStatus.ERROR
                        result_severity = EventSeverity.HIGH

                    event_end = FileEvent(
                        file=model_instance,
                        service=service,
                        subject=result_subject,
                        details=result_msg,
                        status=result_status,
                        severity=result_severity,
                        originator_user=model_instance.updater or model_instance.creator
                    )
                    event_end.save()

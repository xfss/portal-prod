from datetime import datetime

import pendulum
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_noop as _

from status.file_router import route_file
from status.models import File, FileEvent, EventStatus, EventSeverity, EventChannel, Edition


@receiver(post_save, sender=File)
def file_saved(sender, instance, created, **kwargs):
    if created:
        file_event = FileEvent(
            file=instance,
            service=None,
            channel=EventChannel.FILE_UPLOAD,
            subject=_('File uploaded'),
            details=_('File uploaded successfully.'),
            timestamp=datetime.now(),
            status=EventStatus.SUCCESS,
            severity=EventSeverity.INFO,
            originator_user=instance.creator
        )
    else:
        file_event = FileEvent(
            file=instance,
            service=None,
            channel=EventChannel.FILE_UPLOAD,
            subject=_('File Updated'),
            details=_('File updated successfully.'),
            timestamp=datetime.now(),
            status=EventStatus.SUCCESS,
            severity=EventSeverity.INFO,
            originator_user=instance.creator
        )
    file_event.save()

    if instance.category == File.EDITION:
        # Save edition for file if it's not yet present
        try:
            edition = instance.edition
        except ObjectDoesNotExist:
            date = pendulum.parse(instance.filename[0:8]).date()
            try:
                edition = Edition.objects.get(date=date)
                try:
                    if instance != edition.file:
                        raise Exception('There is already a file uploaded to this edition.')
                except ObjectDoesNotExist:
                    # This is expected as we only want to assign edition to file if there is none
                    pass
            except ObjectDoesNotExist:
                edition = Edition(date=date)

        edition.publication = instance.publication
        edition.file = instance
        edition.save()

    route_file(instance)

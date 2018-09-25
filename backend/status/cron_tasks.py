import logging

import pendulum

from status.models import Schedule, File, Edition, ScheduleEvent, EventSeverity, EventStatus, EventChannel

logger = logging.getLogger('cron_task')
logger.setLevel(logging.ERROR)


def check_edition_schedules():
    for schedule in Schedule.objects.all():
        current_time = pendulum.today().subtract(seconds=1)
        next_occurrence = pendulum.instance(schedule.recurrence.after(current_time, dtstart=current_time))
        if next_occurrence.is_today():
            files = File.objects.filter(edition__date=pendulum.today(), publication=schedule.publication)
            if files:
                # TODO: service push in the future??
                pass
            else:
                logger.warning('No file found schedule(s)! Sending out notifications.')

                edition = Edition(date=pendulum.today(), publication=schedule.publication)
                edition.save()
                event = ScheduleEvent(schedule=schedule, edition=edition, severity=EventSeverity.HIGH, status=EventStatus.ERROR, channel=EventChannel.SCHEDULE_MISSED)
                event.save()

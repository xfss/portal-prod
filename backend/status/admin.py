from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from status.models import (
    File, FileEvent, Notification, Service, ServiceEvent, Schedule,
    Edition)


class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'friendly_name',
        'address',
        'port',
        'parameters',
        'secure_parameters',
        'filename_pattern',
        'type',
        'created_at',
        'updated_at',
        'creator',
        'updater',
    )
    filter_horizontal = ('publication',)


class ServiceEventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'service',
        'details',
        'timestamp',
    )

class EditionInline(admin.StackedInline):
    model = Edition
    can_delete = False
    readonly_fields = ('created_at', 'updated_at')

class FileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'file',
        'filename',
        'edition_date',
        'created_at',
        'updated_at',
        'creator',
        'updater',
        'publication'
    )
    excluded_from_new = (
        'filename',
    )
    readonly_fields = ('creator', 'updater', 'created_at', 'updated_at')
    inlines = (EditionInline,)

    def get_exclude(self, request, obj=None):
        if obj:
            return self.exclude or () + getattr(self, 'excluded_from_update', ())
        else:
            return self.exclude or () + getattr(self, 'excluded_from_new', ())

    def edition_date(self, obj):
        return obj.edition.date if obj.edition else None

class FileEventAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'file',
        'service',
        'subject',
        'details',
        'timestamp',
        'originator_user',
        'originator_service',
    )


class ScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'publication',
    )

    list_display_links = (
        'id',
        'name',
    )

    class Media:
        css = {
            'all': (
                staticfiles_storage.url('recurrence/css/recurrence.css'),
            ),
        }
        js = (
            staticfiles_storage.url('recurrence/js/recurrence.js'),
            staticfiles_storage.url('recurrence/js/recurrence-widget.js'),
        )


class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'publication',
        'subject',
        'status',
        'severity',
        'timestamp'
    )


admin.site.register(Service, ServiceAdmin)
admin.site.register(ServiceEvent, ServiceEventAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(FileEvent, FileEventAdmin)
admin.site.register(Schedule, ScheduleAdmin)
admin.site.register(Notification, NotificationAdmin)

from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError

from portal.models import Settings, Publication, Membership, Publisher, PublisherMembership, PublicationConfigRule

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from portal.validators import publication_config_validator
from status.models import NotificationSubscription, PublicationService


class SettingsInline(admin.StackedInline):
    model = Settings
    can_delete = False
    verbose_name_plural = 'Settings'


class NotificationSubscriptionInline(admin.TabularInline):
    model = NotificationSubscription
    can_delete = True
    extra = 2
    verbose_name_plural = 'Notification Subscriptions'


class CustomUserAdmin(UserAdmin):
    inlines = (SettingsInline, NotificationSubscriptionInline)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class PublisherMembershipInline(admin.TabularInline):
    model = PublisherMembership
    extra = 1


class PublisherAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'billing_vat_code',
    )
    inlines = (PublisherMembershipInline,)


class MembershipInline(admin.TabularInline):
    model = Membership
    extra = 1

    readonly_fields = ('creator',)


class PublicationServiceInline(admin.TabularInline):
    model = PublicationService
    extra = 0


class PublicationAdminForm(forms.ModelForm):
    def clean_configuration(self):
        return publication_config_validator(self.cleaned_data['configuration'], exception_to_raise=ValidationError)


class PublicationAdmin(admin.ModelAdmin):
    form = PublicationAdminForm
    list_display = (
        'id',
        'name',
        'code',
        'filename_pattern',
        'language',
        'timezone',
        'configuration'
    )
    inlines = (MembershipInline, PublicationServiceInline)

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for instance in instances:
            if isinstance(instance, Membership) and not instance.id:
                instance.creator = request.user
            instance.save()
        formset.save()


class PublicationConfigRuleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'path',
        'type',
        'mandatory'
    )

admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(PublicationConfigRule, PublicationConfigRuleAdmin)

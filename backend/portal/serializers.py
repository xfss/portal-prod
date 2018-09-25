from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from fields.language import LocalizedDateTimeField
from helpers.language import get_user_lang
from portal.models import (
    LocaleSettingsBase, Membership, Publication, Publisher,
    PublisherMembership, PublicationConfigRule)
from portal.validators import publication_config_validator
from status.models import Schedule

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    publications = serializers.SerializerMethodField()
    language = serializers.SerializerMethodField()
    is_publication_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        exclude = ('id', 'password',)

    @staticmethod
    def get_publications(obj):
        if obj.is_staff:
            query = Publication.objects.all()
        else:
            query = Publication.objects.filter(membership__user=obj)

        publications = []
        for publication in query.order_by('name'):
            scheduled_days = []
            for s in Schedule.objects.filter(publication=publication):
                for rule in s.recurrence.rrules:
                    for d in rule.byday:
                        if d.weekday not in scheduled_days:
                            scheduled_days.append(d.weekday)

            publications.append({
                'id': publication.id,
                'name': publication.name,
                'pattern': publication.filename_pattern,
                'scheduled_days': sorted(scheduled_days)
            })

        return publications

    @staticmethod
    def get_is_publication_admin(obj):
        """

        Determines if the user have publication admin privileges to any publication.

        :return: bool
        """
        # Staff always have publication admin privileges
        if obj.is_staff:
            return True

        return Publication.objects.filter(membership__user=obj, membership__role=Membership.ADMIN).count() > 0

    def get_language(self, obj):
        return get_user_lang(self.context['request'])


class UserBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email')


class PublisherUserSerializer(serializers.ModelSerializer):
    is_primary_contact = serializers.SerializerMethodField()
    is_project_manager = serializers.SerializerMethodField()
    user = UserBriefSerializer(read_only=True)

    created_at = LocalizedDateTimeField(read_only=True)
    updated_at = LocalizedDateTimeField(read_only=True)

    class Meta:
        model = PublisherMembership
        fields = '__all__'

    @staticmethod
    def get_is_primary_contact(obj):
        return bool(obj.is_primary_contact)

    @staticmethod
    def get_is_project_manager(obj):
        return bool(obj.is_project_manager)


class PublisherSerializer(serializers.ModelSerializer):
    language_name = serializers.ChoiceField(choices=settings.LANGUAGES, source='get_language_display', required=False)
    timezone_name = serializers.ChoiceField(choices=LocaleSettingsBase.TIMEZONE_CHOICES, source='get_timezone_display', required=False)
    members = PublisherUserSerializer(many=True, read_only=True, required=False)

    created_at = LocalizedDateTimeField(read_only=True)
    updated_at = LocalizedDateTimeField(read_only=True)

    class Meta:
        model = Publisher
        fields = '__all__'


class PublicationBriefSerializer(serializers.ModelSerializer):
    language = serializers.ChoiceField(choices=settings.LANGUAGES, source='get_language_display', read_only=True)
    timezone = serializers.ChoiceField(choices=LocaleSettingsBase.TIMEZONE_CHOICES, source='get_timezone_display', read_only=True)

    class Meta:
        model = Publication
        fields = ('id', 'name', 'code', 'website_url', 'logo', 'language', 'timezone')


class PublicationSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()
    language_name = serializers.ChoiceField(choices=settings.LANGUAGES, source='get_language_display', required=False)
    timezone_name = serializers.ChoiceField(choices=LocaleSettingsBase.TIMEZONE_CHOICES, source='get_timezone_display', required=False)
    members = UserBriefSerializer(many=True, read_only=True)

    class Meta:
        model = Publication
        fields = '__all__'

    def get_role(self, obj):
        try:
            own_membership = Membership.objects.get(publication=obj, user=self.context['request'].user)
            return own_membership.get_role_display()
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def validate_configuration(value):
        return publication_config_validator(value, exception_to_raise=serializers.ValidationError)


class PublicationConfigRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicationConfigRule
        fields = '__all__'

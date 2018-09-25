from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils.functional import cached_property
from django.utils.translation import gettext_noop as _
from dry_rest_permissions.generics import allow_staff_or_superuser
from pendulum import timezones

from storages.backends.s3boto3 import S3Boto3Storage

User = get_user_model()


class LocaleSettingsBase(models.Model):
    """

    Base class for locale related settings.

    """
    TIMEZONE_CHOICES = [(i, timezone) for i, timezone in enumerate(timezones)]

    language = models.CharField(max_length=10, choices=settings.LANGUAGES, null=True, blank=True)
    timezone = models.IntegerField(choices=TIMEZONE_CHOICES, null=True, blank=True)

    class Meta:
        abstract = True


class Settings(LocaleSettingsBase):
    """

    Settings for Django's User model.

    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    salutation = models.CharField(max_length=20, null=True, blank=True)


class Publisher(LocaleSettingsBase):
    """

    The publisher model represents a customer or company, who in turn can have more than one publication belonging to it.

    """
    name = models.CharField(max_length=255, null=False, blank=False)

    billing_vat_code = models.CharField(max_length=255, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @cached_property
    def primary_contact(self):
        membership = self.members.filter(is_primary_contact=True).first()
        if membership:
            return membership.user

        first_member = self.members.filter(is_contact=True).first()
        if first_member:
            return first_member.user

        return

    @property
    def newspaper_codes_list(self):
        return [publication.code for publication in self.publications.all()]

    @cached_property
    def has_adfusion(self):
        return hasattr(self, 'adfusion_contract')

    @cached_property
    def has_newsfusion(self):
        from crm.models import NewsfusionContract
        return hasattr(self, 'newsfusion_contract')

    def __str__(self):
        return self.name

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return self.members.filter(user=request.user).count() > 0

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    @allow_staff_or_superuser
    def has_create_permission(self, request):
        return False


class PublisherMembership(models.Model):
    """

    This model represents the many to many connection between Publishers and Users.
    Currently this is only used for contact detail handling, but in the future this will be a more general model and keeping track of publisher contacts will be just a  part of it.

    """
    publisher = models.ForeignKey(Publisher, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_contact = models.BooleanField(default=False, help_text="Designates if this member of the publisher should be considered as a contact or not.")
    is_primary_contact = models.NullBooleanField(
        choices=((True, 'True'), (None, 'False')),
        help_text="If a contract doesn't have a contact user set the member with this flag will be used for invoice contact details. A publisher can only have a single primary contact."
    )

    is_project_manager = models.NullBooleanField(
        choices=((True, 'True'), (None, 'False')),
        help_text='A publisher can only have a single project manager.'
    )

    collaboration_grade = models.IntegerField(null=True, blank=True)
    position = models.CharField(max_length=200, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (('publisher', 'is_primary_contact'), ('publisher', 'is_project_manager'))

    def save(self, *args, **kwargs):
        if self.is_primary_contact is False:
            self.is_primary_contact = None

        if self.is_project_manager is False:
            self.is_project_manager = None

        super().save(*args, **kwargs)

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    @allow_staff_or_superuser
    def has_create_permission(self, request):
        return False


class Publication(LocaleSettingsBase):
    """

    This model represents a newspaper or any other type of publication.
    It can (and should) have a publisher associated with it to keep track of higher level information regarding it like company details, invoices, etc.

    """

    publisher = models.ForeignKey(Publisher, related_name='publications', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False, blank=False)
    code = models.CharField(max_length=50, null=True, blank=True)
    members = models.ManyToManyField(User, through='Membership', through_fields=('publication', 'user'))
    filename_pattern = models.CharField(max_length=500, null=True)

    website_url = models.CharField(max_length=200, null=True, blank=True)
    editions_per_year = models.IntegerField(null=True, blank=True)
    printed_pages_per_year = models.IntegerField(null=True, blank=True, help_text='Number of printed pages per year.')
    circulation = models.IntegerField(null=True, blank=True, help_text='Number of copies distributed per edition.')
    logo = models.FileField(null=True, blank=True, storage=S3Boto3Storage(bucket='publication-logo'))
    configuration = JSONField(blank=True, default={})

    def __str__(self):
        return f'Publication: {self.name} (id: {self.id})'

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return self.membership_set.filter(user=request.user, role=Membership.ADMIN).count() > 0

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return self.membership_set.filter(user=request.user, role=Membership.ADMIN).count() > 0

    @allow_staff_or_superuser
    def has_create_permission(self, request):
        return False

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    creator = models.ForeignKey(to=User, related_name='%(class)s_creator', null=True, on_delete=models.SET_NULL)

    # Role field
    ADMIN = 0
    FILE_UPLOADER = 1
    ROLE_CHOICES = (
        (ADMIN, _('Admin')),
        (FILE_UPLOADER, _('File Uploader')),
    )
    role = models.IntegerField(choices=ROLE_CHOICES)


class PublicationConfigRule(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, help_text='Name of field. Only used for clarity, not used for validation.')
    path = models.CharField(max_length=200, unique=True, null=False, blank=False, help_text='Dot notated path of configuration field.')

    BOOLEAN = 'bool'
    STRING = 'str'
    INT = 'int'
    FLOAT = 'float'
    LIST = 'list'

    # For Django choice fields
    TYPE_CHOICES = (
        (BOOLEAN, _('Boolean')),
        (STRING, _('String')),
        (INT, _('Integer')),
        (FLOAT, _('Float')),
        (LIST, _('List')),
    )
    # If type is not set it means type is not enforced, can be anything
    type = models.CharField(max_length=200, choices=TYPE_CHOICES, null=True, blank=True, help_text='Type of configuration field. If set it will be enforced. If not set it can be anything.')
    mandatory = models.BooleanField(null=False, blank=False, default=False, help_text='Is this field mandatory?')

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    @allow_staff_or_superuser
    def has_create_permission(self, request):
        return False

from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_noop as _
from dry_rest_permissions.generics import allow_staff_or_superuser

from portal.models import Publisher, Publication

User = get_user_model()


class Contract(models.Model):
    """

    This model is the base of all more specific contract models, and contains common data relevant to all contract types.

    """
    publications = models.ManyToManyField(Publication)
    contact = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE,
        help_text="If set, the selected user's data will be inserted in the invoice contact fields. This takes precedence over the publisher's contact fields."
    )

    code = models.CharField(max_length=10, null=True, blank=True, help_text="Used for invoice number generation instead of publisher/publication code.")

    activation_date = models.DateField()
    deactivation_date = models.DateField(null=True, blank=True)

    class Meta:
        abstract = True

    def active_for_invoice(self, start, end):
        if isinstance(start, datetime):
            start = start.date()
        if isinstance(end, datetime):
            end = end.date()
        return self.activation_date < end and (not self.deactivation_date or self.deactivation_date > start)

    @property
    def publication_codes(self):
        return tuple(p.code for p in self.publications.all())

    @property
    def publication_names(self):
        return tuple(p.name for p in self.publications.all())

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return False

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    @allow_staff_or_superuser
    def has_create_permission(self, request):
        return False


class AdfusionContract(Contract):
    """

    This contract type contains information for AdFusion invoice generation.

    """
    publisher = models.ForeignKey(Publisher, related_name='adfusion_contract', on_delete=models.CASCADE)

    processing_fee = models.FloatField()  # min 0
    monthly_base_fee = models.FloatField(null=True, blank=True)

    nonrevenue_discount_pct = models.FloatField(
        null=True, blank=True,
        verbose_name=_('Ads non-revenue discount percentage'),
        help_text=_('Discount for processing of non-revenue ads. Applied as a percentage to all ads. Decimal value in range [0-100]'),
    )  # min 0 max 1

    general_discount_pct = models.FloatField(
        verbose_name=_('General discount percentage'),
        help_text=_('Discount percentage applied to all billed AdFusion items. Decimal value in range [0-100]'),
        null=True, blank=True
    )  # min 0 max 1

    BILL_PUBLISHED_REVENUE = 'published_revenue'
    BILL_ALL = 'all'
    BILLED_ADS_CHOICES = (
        (BILL_PUBLISHED_REVENUE, _('Only published ads with revenue')),
        (BILL_ALL, _('All ads')),
    )
    billed_ads = models.CharField(max_length=30, choices=BILLED_ADS_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NewsfusionContract(Contract):
    """

    This contract type contains information for NewsFusion invoice generation.

    """
    publisher = models.ForeignKey(Publisher, related_name='newsfusion_contract', on_delete=models.CASCADE)

    page_fee = models.FloatField()
    discount_pct = models.FloatField(null=True, blank=True)

    BILL_PER_PAGE = 'per_page'
    BILL_PER_PROCESSED_PAGE = 'per_processed_page'
    BILLED_PAGES_CHOICES = (
        (BILL_PER_PAGE, _('All pages of edition.')),
        (BILL_PER_PROCESSED_PAGE, _('Only news pages.')),
    )
    billed_pages = models.CharField(max_length=30, choices=BILLED_PAGES_CHOICES)


class Invoice(models.Model):
    """

    The base invoice model, which contains general invoice related information.

    """
    publisher = models.ForeignKey(Publisher, related_name='invoices', on_delete=models.PROTECT)
    publications = models.ManyToManyField(Publication, related_name='invoices')

    invoice_number = models.CharField(max_length=255, unique=True)

    invoice_date = models.DateField()
    invoice_start_date = models.DateField()
    invoice_end_date = models.DateField()
    invoice_due_date = models.DateField()

    vat_number = models.CharField(max_length=255)
    vat_pct = models.FloatField(null=True, blank=True)
    vat_total = models.FloatField(null=True, blank=True)
    pre_vat_total = models.FloatField(null=True, blank=True)

    exact_total = models.FloatField(null=True, blank=True)
    final_total = models.FloatField(null=True, blank=True)

    document = models.FileField(null=True, blank=True)

    contact_salutation = models.CharField(max_length=100, null=True, blank=True)
    contact_full_name = models.CharField(max_length=255)
    contact_billing_address = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    PRODUCT_ADFUSION = 'adfusion'
    PRODUCT_NEWSFUSION = 'newsfusion'
    PRODUCT_CHOICES = (
        (PRODUCT_ADFUSION, _('AdFusion')),
        (PRODUCT_NEWSFUSION, _('NewsFusion')),
    )
    product = models.CharField(max_length=255, choices=PRODUCT_CHOICES)

    STATUS_PENDING = 'pending'
    STATUS_CANCELLED = 'cancelled'
    STATUS_PAID = 'paid'
    STATUS_CHOICES = (
        (STATUS_PENDING, _('Pending')),
        (STATUS_CANCELLED, _('Cancelled')),
        (STATUS_PAID, _('Paid')),
    )
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default=STATUS_PENDING)

    @property
    def is_pending(self):
        return self.status == self.STATUS_PENDING

    @property
    def is_cancelled(self):
        return self.status == self.STATUS_CANCELLED

    @property
    def is_paid(self):
        return self.status == self.STATUS_PAID

    @property
    def is_adfusion(self):
        return self.product == self.PRODUCT_ADFUSION

    @property
    def is_newsfusion(self):
        return self.product == self.PRODUCT_NEWSFUSION

    @property
    def publication_codes(self):
        return tuple(p.code for p in self.publications.all())

    @property
    def publication_names(self):
        return tuple(p.name for p in self.publications.all())

    @allow_staff_or_superuser
    def has_object_read_permission(self, request):
        return self.publisher and self.publisher.members.filter(user=request.user).count() > 0

    @allow_staff_or_superuser
    def has_object_write_permission(self, request):
        return False

    @staticmethod
    def has_create_permission(request):
        return False

    def __str__(self):
        return f'{self.invoice_number}'


class AdFusionInvoice(models.Model):
    """

    One to one joined model for invoices to keep track of AdFusion specific information.

    """
    invoice = models.OneToOneField(Invoice, related_name='adfusion', on_delete=models.CASCADE)

    monthly_base_fee = models.FloatField(null=True, blank=True)
    processing_fee = models.FloatField(default=0)
    ad_count = models.PositiveIntegerField(default=0)
    processing_total = models.FloatField(default=0)

    nonrevenue_discount_pct = models.FloatField(null=True, blank=True)
    nonrevenue_discount_total = models.FloatField(null=True, blank=True)

    pre_general_discount_total = models.FloatField(default=0)

    general_discount_pct = models.FloatField(null=True, blank=True)
    general_discount_total = models.FloatField(null=True, blank=True)

    total = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AdFusionInvoiceDay(models.Model):
    """

    Model to keep track of counts for each day in relation to an AdFusion invoice.

    """
    adfusion = models.ForeignKey(AdFusionInvoice, related_name='days', on_delete=models.CASCADE)

    date = models.DateField()

    ad_count = models.PositiveIntegerField()
    processing_total = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)


class NewsFusionInvoice(models.Model):
    """

    One to one joined model for invoices to keep track of NewsFusion specific information.

    """
    invoice = models.OneToOneField(Invoice, related_name='newsfusion', on_delete=models.CASCADE)

    page_fee = models.FloatField(default=0)
    pre_discount_total = models.FloatField(default=0)
    discount_pct = models.FloatField(default=0)
    discount_total = models.FloatField(default=0)

    # Based on page count method choice
    page_count = models.PositiveIntegerField(default=0)

    total = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NewsFusionInvoiceDay(models.Model):
    """

    Model to keep track of counts for each day in relation to an AdFusion invoice.

    """
    newsfusion = models.ForeignKey(NewsFusionInvoice, related_name='days', on_delete=models.CASCADE)

    date = models.DateField()

    page_count = models.PositiveIntegerField()
    processing_total = models.FloatField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('date',)

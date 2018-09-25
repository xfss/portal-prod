import logging
import time
import textwrap
from datetime import datetime, timedelta

from django.conf import settings
from django.core.files.base import ContentFile
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone, translation
from weasyprint import HTML

from portal.models import Publisher
from crm.models import Invoice, AdFusionInvoice, AdFusionInvoiceDay, NewsFusionInvoice, AdfusionContract, NewsfusionContract, NewsFusionInvoiceDay
from services.fusion import FusionBackend

logger = logging.getLogger(__name__)


def create_all_invoices(product=None):
    """
    Generates invoices for all publishers for the previous month.

    Original function written by mbitzi, under create_monthly_invoices(),
    but doesn't match our process of using the entire month

    """
    today = timezone.now().date()
    end_date = today.replace(day=1) - timedelta(days=1)
    start_date = end_date.replace(day=1)
    invoice_date = end_date

    for publisher in Publisher.objects.iterator():
        create_invoices_for_publisher(publisher, start_date, end_date, invoice_date, product=product)


def create_invoices_for_publisher(publisher, start_date, end_date, invoice_date, product=None):
    invoices = []
    if product is None or product == Invoice.PRODUCT_ADFUSION:
        for contract in publisher.adfusion_contract.all():
            if not contract.active_for_invoice(start_date, end_date):
                continue

            invoice = create_invoice(publisher, Invoice.PRODUCT_ADFUSION, start_date, end_date, invoice_date, contract=contract)
            invoices.append(invoice)

    if product is None or product == Invoice.PRODUCT_NEWSFUSION:
        for contract in publisher.newsfusion_contract.all():
            if not contract.active_for_invoice(start_date, end_date):
                continue

            invoice = create_invoice(publisher, Invoice.PRODUCT_NEWSFUSION, start_date, end_date, invoice_date, contract=contract)
            invoices.append(invoice)
    return invoices


@transaction.atomic()
def create_invoice(publisher, product, invoice_start_date, invoice_end_date, invoice_date, contract):
    """Generates an invoice for the given publisher and date range."""

    # Contacts will be generated in the following order of preference: contact of contract -> primary contact of publisher > first contact of publisher
    if contract.contact:
        contact = contract.contact
    else:
        if not publisher.primary_contact:
            raise ValueError('Publisher has no contacts defined.')
        contact = publisher.primary_contact

    if product == Invoice.PRODUCT_ADFUSION and not publisher.has_adfusion:
        raise ValueError('Publisher does not have AdFusion configured.')

    if product == Invoice.PRODUCT_NEWSFUSION and not publisher.has_newsfusion:
        raise ValueError('Publisher does not have NewsFusion configured.')

    invoice_due_date = _get_invoice_due_date(invoice_date)

    # TODO: contact_full_name is generated from first name last name, should we add a full_name field to handle special cases?
    invoice = Invoice(publisher=publisher,
                      product=product,
                      contact_salutation=contact.settings.salutation,
                      contact_full_name=f"{contact.first_name} {contact.last_name}",
                      contact_billing_address=contact.settings.address,
                      invoice_date=invoice_date,
                      invoice_start_date=invoice_start_date,
                      invoice_end_date=invoice_end_date,
                      invoice_due_date=invoice_due_date,
                      invoice_number=_generate_invoice_number(contract, publisher),
                      vat_number=publisher.billing_vat_code,
                      vat_pct=settings.VAT_PCT,
                      pre_vat_total=0,
                      vat_total=0,
                      exact_total=0,
                      final_total=0)

    invoice.full_clean()
    invoice.save()
    invoice.publications.set(contract.publications.all())

    if product == Invoice.PRODUCT_ADFUSION:
        _calculate_adfusion(invoice, contract)
    elif product == Invoice.PRODUCT_NEWSFUSION:
        _calculate_newsfusion(invoice, contract)
    else:
        raise Exception(f'Invoice generation error: Unknown invoice product: {product}')

    _calculate_invoice_totals(invoice)

    invoice.full_clean()
    invoice.save()

    _generate_invoice_pdf(invoice, contract)

    return invoice


def _calculate_adfusion(invoice, contract):
    """Calculates the totals as well as discounts for adfusion processing.

    The discount is based on the price for all ads minus the discount.
    The actual amount of non-revenue ads is not relevant for the price calculation.

    Also generates a per-day breakdown for processed ads.
    """
    if invoice.product != Invoice.PRODUCT_ADFUSION or not invoice.publisher.has_adfusion:
        return

    reports = [FusionBackend().query_newspaper_report(publication.code, invoice.invoice_start_date, invoice.invoice_end_date) for publication in contract.publications.all()]

    adfusion = _create_adfusion_base(invoice, contract, reports)
    _create_adfusion_days(adfusion, contract, reports)


def _calculate_newsfusion(invoice, contract):
    if invoice.product != Invoice.PRODUCT_NEWSFUSION or not invoice.publisher.has_newsfusion:
        return

    reports = [FusionBackend().query_newspaper_report(publication.code, invoice.invoice_start_date, invoice.invoice_end_date) for publication in contract.publications.all()]
    newsfusion = _create_newsfusion_base(invoice, contract, reports)
    if newsfusion:
        _create_newsfusion_days(newsfusion, contract, reports)


def _create_adfusion_base(invoice, contract, reports):
    """Creates an adfusion invoice for the given reports."""
    # We should create an empty invoice even if the contract was not active during that time.
    adfusion = AdFusionInvoice(invoice=invoice)
    adfusion.full_clean()
    adfusion.save()

    if not contract.active_for_invoice(invoice.invoice_start_date, invoice.invoice_end_date):
        return

    adfusion.monthly_base_fee = contract.monthly_base_fee

    adfusion.ad_count = sum(_count_billed_ads(contract, r.ads) for r in reports)

    adfusion.processing_fee = contract.processing_fee
    adfusion.processing_total = round(contract.processing_fee * adfusion.ad_count, 2)

    if contract.nonrevenue_discount_pct:
        adfusion.nonrevenue_discount_pct = contract.nonrevenue_discount_pct
        adfusion.nonrevenue_discount_total = round(adfusion.processing_total * adfusion.nonrevenue_discount_pct, 2)
    else:
        adfusion.nonrevenue_discount_pct = None
        adfusion.nonrevenue_discount_total = None

    total = ((adfusion.monthly_base_fee or 0)
             + adfusion.processing_total
             - (adfusion.nonrevenue_discount_total or 0))

    adfusion.pre_general_discount_total = round(total, 2)

    if contract.general_discount_pct:
        adfusion.general_discount_pct = contract.general_discount_pct
        adfusion.general_discount_total = round(adfusion.pre_general_discount_total * adfusion.general_discount_pct, 2)
        total -= adfusion.general_discount_total

    adfusion.total = total

    adfusion.full_clean()
    adfusion.save()

    return adfusion


def _create_adfusion_days(adfusion, contract, reports):
    """Generates a per-day breakdown for the given invoice."""
    invoice = adfusion.invoice
    all_editions = [e for r in reports for e in r.editions]

    if not all_editions:
        return

    for i in range((invoice.invoice_end_date - invoice.invoice_start_date).days + 1):
        current_date = invoice.invoice_start_date + timedelta(days=i)
        day_editions = list(filter(lambda e: e.edition_date == current_date, all_editions))

        if not day_editions:
            continue

        ad_count = sum(_count_billed_ads(contract, e.ads) for e in day_editions)
        processing_total = round(adfusion.processing_fee * ad_count, 2)

        day = AdFusionInvoiceDay(adfusion=adfusion,
                                 date=current_date,
                                 ad_count=ad_count,
                                 processing_total=processing_total)
        day.full_clean()
        day.save()


def _create_newsfusion_base(invoice, contract, reports):
    """Creates an newsfusion invoice for the given reports."""
    # We should create an empty invoice even if the contract was not active during that time.
    newsfusion = NewsFusionInvoice(invoice=invoice)
    newsfusion.full_clean()
    newsfusion.save()

    if not contract.active_for_invoice(invoice.invoice_start_date, invoice.invoice_end_date):
        return

    newsfusion.page_fee = contract.page_fee
    newsfusion.discount_pct = contract.discount_pct or 0

    newsfusion.page_count = sum(_count_billed_pages(contract, report.news) for report in reports)

    newsfusion.pre_discount_total = round(float(newsfusion.page_count) * newsfusion.page_fee, 2)
    newsfusion.discount_total = round(newsfusion.pre_discount_total * newsfusion.discount_pct, 2)
    newsfusion.total = newsfusion.pre_discount_total - newsfusion.discount_total

    newsfusion.full_clean()
    newsfusion.save()

    return newsfusion


def _create_newsfusion_days(newsfusion, contract, reports):
    """Generates a per-day breakdown for the given invoice."""
    invoice = newsfusion.invoice
    all_editions = [e for r in reports for e in r.editions]

    if not all_editions:
        return

    for i in range((invoice.invoice_end_date - invoice.invoice_start_date).days + 1):
        current_date = invoice.invoice_start_date + timedelta(days=i)
        day_editions = list(filter(lambda e: e.edition_date == current_date, all_editions))

        # Some Editions received from Fusion have ADS but no news
        # and the reporting here defaults both `news_pages` and
        # `total_pages` to 0 if no news is found in an Edition
        for day in day_editions:
            if not day.news.total_pages and not day.news.news_pages:
                day_editions.remove(day)

        if not day_editions:
            continue

        page_count = sum(_count_billed_pages(contract, e.news) for e in day_editions)
        processing_total = round(newsfusion.page_fee * page_count, 2)

        day = NewsFusionInvoiceDay(newsfusion=newsfusion,
                                   date=current_date,
                                   page_count=page_count,
                                   processing_total=processing_total)
        day.full_clean()
        day.save()


def _count_billed_ads(contract, ads):
    if contract.billed_ads == AdfusionContract.BILL_ALL:
        return ads.total
    elif contract.billed_ads == AdfusionContract.BILL_PUBLISHED_REVENUE:
        return ads.published_revenue
    else:
        raise ValueError('Invalid configuration for `billed_ads`')


def _count_billed_pages(contract, pages):
    if contract.billed_pages == NewsfusionContract.BILL_PER_PAGE:
        return pages.total_pages
    elif contract.billed_pages == NewsfusionContract.BILL_PER_PROCESSED_PAGE:
        return pages.news_pages
    else:
        raise Exception(f'Unknown billed page type for NewsfusionContract. id: {contract.id}')


def _get_invoice_due_date(invoice_date):
    """Return whichever date comes sooner."""
    invoice_due_date1 = invoice_date + settings.INVOICES_DUE_DELTA
    invoice_due_date2 = last_day_of_next_month(invoice_date)
    return min(invoice_due_date1, invoice_due_date2)


def _calculate_invoice_totals(invoice):
    """Calculates the final vat and totals for the given invoice."""
    if invoice.product == Invoice.PRODUCT_ADFUSION:
        invoice.pre_vat_total = invoice.adfusion.total
    elif invoice.product == Invoice.PRODUCT_NEWSFUSION:
        invoice.pre_vat_total = invoice.newsfusion.total

    invoice.vat_total = round(invoice.pre_vat_total * invoice.vat_pct, 2)
    invoice.exact_total = round(invoice.pre_vat_total + invoice.vat_total, 2)
    invoice.final_total = round_to_05(invoice.exact_total)

def _get_code(contract):
    code = None
    if contract.code:
        code = contract.code

    if not code:
        publication = contract.publications.exclude(code__isnull=True).exclude(code='').first()
        if publication:
            code = publication.code

    if not code:
        raise Exception("Invoice generation failed. No code for contract and no code can be determined for any of the contract's publications.")
    return code


def _generate_invoice_number(contract, publisher):
    """Generates an unique invoice number.

    Invoice numbers have a fixed format and only ever increase and are therefore sortable.
    """

    code = _get_code(contract)

    for _ in range(100):
        ts = int((datetime.now() - datetime(2010, 1, 1)).total_seconds() * 1000)
        ts = '-'.join(textwrap.wrap(str(ts), width=4))
        invoice_number = "{}-{}".format(code.upper(), ts)

        if not publisher.invoices.filter(invoice_number=invoice_number).exists():
            return invoice_number

        time.sleep(0.001)

    raise Exception(f'Could not generate invoice number for publisher: {publisher.name} (id: {publisher.id}) code used: {code}')


def _generate_invoice_pdf(invoice, contract):
    with translation.override(invoice.publisher.language):
        html = render_to_string('invoices/invoice_pdf.html', {'invoice': invoice})
    logging.getLogger('weasyprint').setLevel(100)
    pdf = HTML(string=html, base_url=settings.BASE_URL).write_pdf()

    if invoice.document:
        invoice.document.delete(save=False)

    filename = f"{invoice.invoice_date.isoformat()}_{invoice.invoice_number}_{invoice.product}.pdf"
    invoice.document.save(filename, ContentFile(pdf))


def last_day_of_month(any_date):
    # select day 28 of given date month, and add 4,
    # ensuring we are in the next month
    next_month = any_date.replace(day=28) + timedelta(days=4)

    # subtract the month day so that we arrive at 0
    return next_month - timedelta(days=next_month.day)


def last_day_of_next_month(any_date):
    # select day 28 of given date month, and add 35 days,
    # ensuring we are two months from given date
    future_month = any_date.replace(day=28) + timedelta(days=35)

    # subtract the month day so that we arrive at 0
    return future_month - timedelta(days=future_month.day)


def round_to_05(n):
    """Rounds a given number to x.x5"""
    precision = 0.05
    correction = 0.5 if n >= 0 else -0.5
    return round(int(n / precision + correction) * precision, 2)

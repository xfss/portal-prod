import re

import coreapi
import coreschema
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import translation
from dry_rest_permissions.generics import DRYObjectPermissions
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, detail_route, renderer_classes, schema
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.renderers import JSONRenderer, StaticHTMLRenderer
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.schemas import ManualSchema
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
import pendulum

from crm.invoices import create_invoice, create_invoices_for_publisher, create_all_invoices
from crm.models import AdfusionContract, NewsfusionContract, Invoice
from crm.serializers import AdfusionContractSerializer, NewsfusionContractSerializer, InvoiceSerializer
from portal.models import Publisher


class AdfusionContractViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AdfusionContract.objects.all()
    serializer_class = AdfusionContractSerializer
    permission_classes = (IsAuthenticated, DRYObjectPermissions,)


class NewsfusionContractViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = NewsfusionContract.objects.all()
    serializer_class = NewsfusionContractSerializer
    permission_classes = (IsAuthenticated, DRYObjectPermissions,)


class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = (IsAuthenticated, DRYObjectPermissions,)

    @detail_route(methods=['get'], renderer_classes=(StaticHTMLRenderer,))
    def html(self, request, pk=None):
        invoice = self.get_object()
        html = render_to_string(
            'invoices/invoice_pdf.html', context={'invoice': invoice}
        )
        regex = re.compile('(?:href=\"/)|(?:src=\"/)', re.IGNORECASE)
        rendered = re.sub(regex, 'href=\"{}/'.format(settings.BASE_URL), html)
        with translation.override(invoice.publisher.language):
            return Response(rendered)


@api_view(['POST'])
@permission_classes((IsAuthenticated, IsAdminUser))
def generate_invoices(request, product=None):
    product_choices = [p[0] for p in Invoice.PRODUCT_CHOICES]
    if product is not None and product not in product_choices:
        return Response(f"Can't generate invoice. Only the following types are possible: {product_choices}", status=HTTP_400_BAD_REQUEST)
    create_all_invoices(product)
    return Response('Invoice generation done.')


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
@schema(ManualSchema(
    fields=[
        coreapi.Field('start_date', required=True, location="query", schema=coreschema.String(description='Get invoice items from this date.')),
        coreapi.Field('end_date', required=True, location="query", schema=coreschema.String(description='Get invoice items to this date.')),
        coreapi.Field('invoice_date', required=True, location="query", schema=coreschema.String(description='Date of invoice.')),
        coreapi.Field(
            'product',
            required=True,
            location="query",
            schema=coreschema.String(description=f'Product for invoice, can be the following: {", ".join([c[0] for c in Invoice.PRODUCT_CHOICES])}')
        ),
    ]
))
@permission_classes((IsAuthenticated, IsAdminUser))
def generate_invoice_for_publisher(request, publisher_id):
    start_date = request.POST.get('start_date')
    if not start_date:
        raise ValidationError('Start date is mandatory!')
    else:
        start_date = pendulum.parse(start_date)

    end_date = request.POST.get('end_date')
    if not end_date:
        raise ValidationError('End date is mandatory!')
    else:
        end_date = pendulum.parse(end_date)

    invoice_date = request.POST.get('invoice_date')
    if not invoice_date:
        raise ValidationError('Invoice date is mandatory!')
    else:
        invoice_date = pendulum.parse(invoice_date)

    product = request.POST.get('product')
    valid_products = [Invoice.PRODUCT_ADFUSION, Invoice.PRODUCT_NEWSFUSION]
    if not invoice_date:
        raise ValidationError('Product is mandatory!')
    elif product not in valid_products:
        raise ValidationError(f'The only valid values for product are the following: {valid_products}')

    publisher = Publisher.objects.get(id=publisher_id)

    invoices = create_invoices_for_publisher(publisher, start_date, end_date, invoice_date, product=product)

    serializer = InvoiceSerializer(invoices, many=True)

    return Response(serializer.data, status=HTTP_201_CREATED)


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
@schema(ManualSchema(
    fields=[
        coreapi.Field('start_date', required=True, location="query", schema=coreschema.String(description='Get invoice items from this date.')),
        coreapi.Field('end_date', required=True, location="query", schema=coreschema.String(description='Get invoice items to this date.')),
        coreapi.Field('invoice_date', required=True, location="query", schema=coreschema.String(description='Date of invoice.')),
        coreapi.Field(
            'product',
            required=True,
            location="query",
            schema=coreschema.String(description=f'Product for invoice, can be the following: {", ".join([c[0] for c in Invoice.PRODUCT_CHOICES])}')
        ),
    ]
))
@permission_classes((IsAuthenticated, IsAdminUser))
def generate_invoice_for_contract(request, contract_id):
    start_date = request.POST.get('start_date')
    if not start_date:
        raise ValidationError('Start date is mandatory!')
    else:
        start_date = pendulum.parse(start_date)

    end_date = request.POST.get('end_date')
    if not end_date:
        raise ValidationError('End date is mandatory!')
    else:
        end_date = pendulum.parse(end_date)

    invoice_date = request.POST.get('invoice_date')
    if not invoice_date:
        raise ValidationError('Invoice date is mandatory!')
    else:
        invoice_date = pendulum.parse(invoice_date)

    product = request.POST.get('product')
    valid_products = [Invoice.PRODUCT_ADFUSION, Invoice.PRODUCT_NEWSFUSION]
    if not invoice_date:
        raise ValidationError('Product is mandatory!')
    elif product not in valid_products:
        raise ValidationError(f'The only valid values for product are the following: {valid_products}')

    if product == Invoice.PRODUCT_ADFUSION:
        contract = AdfusionContract.objects.get(id=contract_id)
    elif product == Invoice.PRODUCT_NEWSFUSION:
        contract = NewsfusionContract.objects.get(id=contract_id)
    else:
        # This should never happen as the validation protects against this...
        raise ValidationError(f'The only valid values for product are the following: {valid_products}')

    invoice = create_invoice(contract.publisher, product, start_date, end_date, invoice_date, contract)

    serializer = InvoiceSerializer(invoice)

    return Response(serializer.data, status=HTTP_201_CREATED)

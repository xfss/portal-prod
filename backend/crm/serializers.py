from rest_framework import serializers

from crm.models import AdfusionContract, NewsfusionContract, Invoice, AdFusionInvoice, AdFusionInvoiceDay
from portal.serializers import UserBriefSerializer, PublicationBriefSerializer, PublisherSerializer


class AdfusionContractSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer(many=False, read_only=True)
    publications = PublicationBriefSerializer(many=True, read_only=True)
    contact = UserBriefSerializer(many=False, read_only=True)

    class Meta:
        model = AdfusionContract
        fields = '__all__'


class NewsfusionContractSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer(many=False, read_only=True)
    publications = PublicationBriefSerializer(many=True, read_only=True)
    contact = UserBriefSerializer(many=False, read_only=True)

    class Meta:
        model = NewsfusionContract
        fields = '__all__'


class AdfusionInvoiceSerializerDay(serializers.ModelSerializer):
    class Meta:
        model = AdFusionInvoiceDay
        fields = ('ad_count', 'date', 'processing_total')
        depth = 0


class AdfusionInvoiceSerializer(serializers.ModelSerializer):
    days = AdfusionInvoiceSerializerDay(many=True, read_only=True)

    class Meta:
        model = AdFusionInvoice
        exclude = ('id', 'invoice')
        depth = 1


class InvoiceSerializer(serializers.ModelSerializer):
    adfusion = AdfusionInvoiceSerializer(many=False, read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'
        read_only_fields = (
            'publisher', 'invoice_number', 'invoice_date', 'invoice_start_date', 'invoice_end_date', 'invoice_due_date', 'vat_number', 'vat_pct', 'vat_total',
            'pre_vat_total', 'exact_total', 'final_total', 'document', 'contact_full_name', 'contact_billing_address', 'created_at', 'updated_at', 'product',
        )
        depth = 1

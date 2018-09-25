from django import forms
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_noop as _

from crm.models import AdfusionContract, Invoice, NewsfusionContract


class ContractAdminForm(forms.ModelForm):
    def clean(self):
        for publication in self.cleaned_data['publications']:
            if publication.publisher != self.cleaned_data['publisher']:
                raise ValidationError({'publications': _(f'All selected publication should belong to the selected publisher.')})

        super().clean()


class AdfusionContractAdmin(admin.ModelAdmin):
    form = ContractAdminForm
    list_display = (
        'id',
        'publisher',
        'publication_codes',
        'processing_fee',
        'monthly_base_fee',
        'nonrevenue_discount_pct',
        'general_discount_pct',
        'billed_ads',
        'activation_date',
        'deactivation_date',
    )
    filter_horizontal = ('publications',)


class NewsfusionContractAdmin(admin.ModelAdmin):
    form = ContractAdminForm
    list_display = (
        'id',
        'publisher',
        'publication_codes',
        'page_fee',
        'discount_pct',
        'billed_pages',
        'activation_date',
        'deactivation_date',
    )
    filter_horizontal = ('publications',)


class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'invoice_number',
        'invoice_date',
        'invoice_start_date',
        'invoice_end_date',
        'publisher',
        'publication_codes',
        'exact_total',
        'final_total',
        'product',
        'status',
    )


admin.site.register(AdfusionContract, AdfusionContractAdmin)
admin.site.register(NewsfusionContract, NewsfusionContractAdmin)
admin.site.register(Invoice, InvoiceAdmin)

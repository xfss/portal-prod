# Generated by Django 2.0.5 on 2018-06-25 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_invoice_publications'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='contact_salutation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
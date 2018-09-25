# Generated by Django 2.0.2 on 2018-05-08 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_auto_20180507_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='adfusioncontract',
            name='code',
            field=models.CharField(blank=True, help_text='Used for invoice number generation instead of publisher/publication code.', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='newsfusioncontract',
            name='code',
            field=models.CharField(blank=True, help_text='Used for invoice number generation instead of publisher/publication code.', max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='adfusioncontract',
            name='contact',
            field=models.ForeignKey(blank=True, help_text="If set, the selected user's data will be inserted in the invoice contact fields. This takes precedence over the publisher's contact fields.", null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='newsfusioncontract',
            name='contact',
            field=models.ForeignKey(blank=True, help_text="If set, the selected user's data will be inserted in the invoice contact fields. This takes precedence over the publisher's contact fields.", null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
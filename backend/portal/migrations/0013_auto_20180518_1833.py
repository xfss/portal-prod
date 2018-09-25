# Generated by Django 2.0.2 on 2018-05-18 18:33

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import storages.backends.s3boto3


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0012_auto_20180508_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='circulation',
            field=models.IntegerField(blank=True, help_text='Number of copies distributed per edition.', null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='configuration',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default={}),
        ),
        migrations.AddField(
            model_name='publication',
            name='editions_per_year',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='logo',
            field=models.FileField(blank=True, null=True, storage=storages.backends.s3boto3.S3Boto3Storage(bucket='publication-logo'), upload_to=''),
        ),
        migrations.AddField(
            model_name='publication',
            name='printed_pages_per_year',
            field=models.IntegerField(blank=True, help_text='Number of printed pages per year.', null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='website_url',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='publishermembership',
            name='collaboration_grade',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='publishermembership',
            name='is_project_manager',
            field=models.NullBooleanField(choices=[(True, 'True'), (None, 'False')], help_text='A publisher can only have a single project manager.'),
        ),
        migrations.AddField(
            model_name='publishermembership',
            name='position',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='publishermembership',
            name='is_primary_contact',
            field=models.NullBooleanField(choices=[(True, 'True'), (None, 'False')], help_text="If a contract doesn't have a contact user set the member with this flag will be used for invoice contact details. A publisher can only have a single primary contact."),
        ),
        migrations.AlterUniqueTogether(
            name='publishermembership',
            unique_together={('publisher', 'is_primary_contact'), ('publisher', 'is_project_manager')},
        ),
    ]
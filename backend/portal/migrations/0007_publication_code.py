# Generated by Django 2.0.2 on 2018-03-16 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_auto_20180307_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
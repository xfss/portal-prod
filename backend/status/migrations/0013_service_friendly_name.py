# Generated by Django 2.0.2 on 2018-03-16 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0012_auto_20180301_1325'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='friendly_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

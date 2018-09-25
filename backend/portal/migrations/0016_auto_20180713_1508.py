# Generated by Django 2.0.5 on 2018-07-13 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0015_settings_salutation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationconfigrule',
            name='path',
            field=models.CharField(help_text='Dot notated path of configuration field.', max_length=200, unique=True),
        ),
    ]

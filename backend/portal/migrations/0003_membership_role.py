# Generated by Django 2.0.2 on 2018-02-22 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_auto_20180221_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='role',
            field=models.IntegerField(choices=[(0, 'Admin'), (1, 'Read Only')], default=1),
            preserve_default=False,
        ),
    ]
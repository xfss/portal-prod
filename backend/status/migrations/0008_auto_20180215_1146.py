# Generated by Django 2.0.2 on 2018-02-15 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0007_service_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='type',
            field=models.IntegerField(choices=[(1, 'SFTP'), (2, 'AboDB'), (3, 'Paperlit')]),
        ),
    ]

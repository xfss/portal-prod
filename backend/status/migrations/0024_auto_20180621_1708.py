# Generated by Django 2.0.5 on 2018-06-21 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0023_scheduleevent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationsubscription',
            name='status',
            field=models.IntegerField(blank=True, choices=[(0, 'Success'), (1, 'In progress'), (2, 'Error')], help_text='Notify about status level equal to this level. Blank sends out notification regardless of status level.', null=True),
        ),
    ]
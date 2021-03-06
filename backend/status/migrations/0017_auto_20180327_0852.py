# Generated by Django 2.0.2 on 2018-03-27 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0008_settings_phone_number'),
        ('status', '0016_auto_20180327_0135'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationService',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('release_offset_time', models.DurationField(blank=True, default=0)),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Publication')),
            ],
        ),
        migrations.RemoveField(
            model_name='service',
            name='publication',
        ),
        migrations.AddField(
            model_name='service',
            name='publication',
            field=models.ManyToManyField(blank=True, through='status.PublicationService', to='portal.Publication'),
        ),
        migrations.AddField(
            model_name='publicationservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='status.Service'),
        ),
        migrations.AlterUniqueTogether(
            name='publicationservice',
            unique_together={('publication', 'service')},
        ),
    ]

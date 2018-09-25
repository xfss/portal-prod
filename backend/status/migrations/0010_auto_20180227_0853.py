# Generated by Django 2.0.2 on 2018-02-27 08:53

from django.db import migrations, models
import django.db.models.deletion
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_publication_filename_pattern'),
        ('status', '0009_auto_20180226_0740'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('recurrence', recurrence.fields.RecurrenceField()),
                ('publication', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='portal.Publication')),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='edition_date',
            field=models.DateField(null=True),
        ),
    ]

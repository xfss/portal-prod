# Generated by Django 2.0.2 on 2018-05-22 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0013_auto_20180518_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicationConfigRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, help_text='Name of field. Only used for clarity, not used for validation.', max_length=200, null=True)),
                ('path', models.CharField(help_text='Dot notated path of configuration field.', max_length=200)),
                ('type', models.CharField(blank=True, choices=[('bool', 'Boolean'), ('str', 'String'), ('int', 'Integer'), ('float', 'Float'), ('list', 'List')], help_text='Type of configuration field. If set it will be enforced. If not set it can be anything.', max_length=200, null=True)),
                ('mandatory', models.BooleanField(default=False, help_text='Is this field mandatory?')),
            ],
        ),
    ]
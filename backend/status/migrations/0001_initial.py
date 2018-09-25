# Generated by Django 2.0.2 on 2018-02-06 07:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(blank=True, max_length=200)),
                ('file', models.FileField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_creator', to=settings.AUTH_USER_MODEL)),
                ('updater', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='file_updater', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FileEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'Success'), (1, 'In progress'), (2, 'Error')])),
                ('file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='status.File')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_creator', to=settings.AUTH_USER_MODEL)),
                ('updater', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_updater', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ServiceEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('details', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(0, 'Up'), (1, 'Down')])),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='status.Service')),
            ],
        ),
        migrations.AddField(
            model_name='fileevent',
            name='originator_service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fileevent_originator_service', to='status.Service'),
        ),
        migrations.AddField(
            model_name='fileevent',
            name='originator_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='fileevent_originator_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='fileevent',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='status.Service'),
        ),
    ]
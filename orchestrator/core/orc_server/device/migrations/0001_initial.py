# Generated by Django 2.2 on 2019-04-04 18:39

import device.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orchestrator', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID of the device', unique=True)),
                ('name', models.CharField(default=device.models.defaultName, help_text='Unique display name of the device', max_length=30, unique=True)),
                ('note', models.TextField(blank=True, help_text='Extra information about the device', null=True)),
            ],
            options={
                'permissions': (('use_device', 'Can use device'),),
            },
        ),
        migrations.CreateModel(
            name='Transport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transport_id', models.CharField(default=device.models.shortID, editable=False, help_text='Unique ID of the transport', max_length=30, unique=True)),
                ('host', models.CharField(default='127.0.0.1', help_text='Hostname/IP of the device', max_length=60)),
                ('port', models.IntegerField(default=8080, help_text='Port of the device')),
                ('exchange', models.CharField(default='exchange', help_text='Exchange for the specific device, only necessary for Pub/Sub protocols', max_length=30)),
                ('routing_key', models.CharField(default='routing_key', help_text='Routing Key for the specific device, only necessary for Pub/Sub protocols', max_length=30)),
                ('protocol', models.ForeignKey(help_text='Protocol supported by the device', on_delete=django.db.models.deletion.CASCADE, to='orchestrator.Protocol')),
                ('serialization', models.ManyToManyField(help_text='Serialization(s) supported by the device', to='orchestrator.Serialization')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Unique display name of the device group', max_length=80, unique=True)),
                ('devices', models.ManyToManyField(blank=True, help_text='Devices available to users in the group', to='device.Device')),
                ('users', models.ManyToManyField(blank=True, help_text='Users in the group', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'group',
                'verbose_name_plural': 'groups',
            },
        ),
        migrations.AddField(
            model_name='device',
            name='transport',
            field=models.ManyToManyField(help_text='Transports the device supports', to='device.Transport'),
        ),
    ]
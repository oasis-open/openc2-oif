# Generated by Django 3.1.1 on 2020-10-14 18:49

from django.db import migrations, models
import django.db.models.deletion

HTTPS_TRANSPORTS = []


def gather_https(apps, schema_editor):
    baseModel = apps.get_model('device', 'transport')
    protocol = apps.get_model('orchestrator', 'protocol').objects.get(name='HTTPS')

    for t in baseModel.objects.filter(protocol=protocol):
        d = dict(
            serialization=[s.pk for s in t.serialization.all()],
            **t.__dict__
        )
        d.pop('_state', None)
        d.pop('polymorphic_ctype_id', None)
        HTTPS_TRANSPORTS.append(d)


def update_https(apps, schema_editor):
    baseModel = apps.get_model('device', 'transport')
    httpsModel = apps.get_model('device', 'transporthttps')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    https_ct = ContentType.objects.get_for_model(httpsModel)

    for data in HTTPS_TRANSPORTS:
        base_trans = baseModel.objects.get(transport_id=data['transport_id'])
        devs = list(base_trans.device_set.all())
        base_trans.delete()
        serials = data.pop('serialization', [])
        trans = httpsModel.objects.create(
            **data,
            polymorphic_ctype=https_ct
        )
        trans.serialization.set(serials)
        trans.save()
        for d in devs:
            d.transport.add(trans)
            d.save()


class Migration(migrations.Migration):

    dependencies = [
        ('device', '0012_transportHTTP_polymorphic'),
    ]

    operations = [
        migrations.RunPython(gather_https, migrations.RunPython.noop),
        migrations.CreateModel(
            name='TransportHTTPS',
            fields=[
                ('transportauth_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='device.transportauth')),
                ('path', models.CharField(blank=True, default='', help_text='URL endpoint path', max_length=60)),
            ],
            options={
                'verbose_name': 'HTTPS Transport',
            },
            bases=('device.transportauth',),
        ),
        migrations.RunPython(update_https, migrations.RunPython.noop),
    ]

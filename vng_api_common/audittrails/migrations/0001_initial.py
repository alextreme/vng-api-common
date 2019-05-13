# Generated by Django 2.0.13 on 2019-05-13 09:31

import uuid

import django.contrib.postgres.fields.jsonb
import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuditTrail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, help_text='Unieke resource identifier (UUID4)', unique=True)),
                ('bron', models.CharField(max_length=50)),
                ('actie', models.CharField(max_length=50)),
                ('actie_weergave', models.CharField(blank=True, max_length=200)),
                ('resultaat', models.IntegerField()),
                ('hoofd_object', models.URLField(max_length=1000)),
                ('resource', models.CharField(max_length=50)),
                ('resource_url', models.URLField(max_length=1000)),
                ('aanmaakdatum', models.DateTimeField(auto_now=True)),
                ('oud', django.contrib.postgres.fields.jsonb.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, null=True)),
                ('nieuw', django.contrib.postgres.fields.jsonb.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder, null=True)),
            ],
        ),
    ]
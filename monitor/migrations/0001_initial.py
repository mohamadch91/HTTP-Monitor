# Generated by Django 4.1.4 on 2023-01-26 16:46

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
            name='Endpoint',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('address', models.URLField(db_index=True)),
                ('fail_limit', models.IntegerField(db_index=True, default=0)),
                ('success_count', models.IntegerField(default=0)),
                ('fail_count', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Endpoint',
            },
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False)),
                ('status_code', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('endpoint', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='monitor.endpoint')),
            ],
            options={
                'db_table': 'Request',
            },
        ),
    ]
# Generated by Django 2.0 on 2020-11-13 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xm', models.CharField(blank=True, max_length=20, null=True)),
                ('pwd', models.CharField(blank=True, max_length=20, null=True)),
                ('xb', models.CharField(blank=True, max_length=2, null=True)),
                ('csny', models.CharField(blank=True, max_length=20, null=True)),
            ],
            options={
                'db_table': 'name',
                'managed': False,
            },
        ),
    ]

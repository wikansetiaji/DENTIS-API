# Generated by Django 2.2 on 2019-04-21 02:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_instansi'),
    ]

    operations = [
        migrations.RenameField(
            model_name='instansi',
            old_name='no_telepon',
            new_name='noTelepon',
        ),
    ]

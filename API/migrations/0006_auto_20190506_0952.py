# Generated by Django 2.2 on 2019-05-06 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_auto_20190505_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='dokter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API.Dokter'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='pasien',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API.Pasien'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='rekam_medis',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='API.RekamMedis'),
        ),
    ]

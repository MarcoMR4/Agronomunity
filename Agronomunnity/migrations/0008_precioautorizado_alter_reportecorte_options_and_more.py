# Generated by Django 4.1 on 2023-05-25 04:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Agronomunnity', '0007_remove_ordencorte_tipofruta_ordencorte_frutahuerta_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrecioAutorizado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precioFijo', models.FloatField(blank=True)),
                ('descripcion', models.CharField(blank=True, max_length=500)),
                ('precioActual', models.FloatField(blank=True)),
                ('vigencia', models.DateField()),
                ('estadoAplica', models.CharField(choices=[('AGS', 'Aguascalientes'), ('BC', 'Baja California'), ('BCS', 'Baja California Sur'), ('CAM', 'Campeche'), ('CHIS', 'Chiapas'), ('CHIH', 'Chihuahua'), ('CDMX', 'Ciudad de México'), ('COAH', 'Coahuila'), ('COL', 'Colima'), ('DGO', 'Durango'), ('GTO', 'Guanajuato'), ('GRO', 'Guerrero'), ('HGO', 'Hidalgo'), ('JAL', 'Jalisco'), ('MEX', 'México'), ('MIC', 'Michoacán'), ('MOR', 'Morelos'), ('NAY', 'Nayarit'), ('NL', 'Nuevo León'), ('OAX', 'Oaxaca'), ('PUE', 'Puebla'), ('QRO', 'Querétaro'), ('QR', 'Quintana Roo'), ('SLP', 'San Luis Potosí'), ('SIN', 'Sinaloa'), ('SON', 'Sonora'), ('TAB', 'Tabasco'), ('TAMPS', 'Tamaulipas'), ('TLAX', 'Tlaxcala'), ('VER', 'Veracruz'), ('YUC', 'Yucatán'), ('ZAC', 'Zacatecas')], default='', max_length=5)),
            ],
            options={
                'verbose_name': 'PrecioAutorizado',
                'verbose_name_plural': 'PreciosAutorizados',
                'db_table': 'precioautorizado',
                'ordering': ['id'],
            },
        ),
        migrations.AlterModelOptions(
            name='reportecorte',
            options={'ordering': ['id'], 'verbose_name': 'ReporteCorte', 'verbose_name_plural': 'ReportesCorte'},
        ),
        migrations.RemoveField(
            model_name='reportecorte',
            name='documento',
        ),
        migrations.AddField(
            model_name='reportecorte',
            name='idViaje',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.viajecorte'),
        ),
        migrations.AlterField(
            model_name='huerta',
            name='frutaHuerta',
            field=models.CharField(choices=[('AGT', 'Aguacate')], default='AGT', max_length=3),
        ),
        migrations.AlterField(
            model_name='huerta',
            name='ubicacionHuerta',
            field=models.CharField(choices=[('UPN', 'Uruapan'), ('SES', 'Salvador Escalante'), ('TAN', 'Tancítaro'), ('PER', 'Peribán'), ('TCM', 'Tacámbaro'), ('ADR', 'Ario de Rosales')], default='UPN', max_length=3),
        ),
        migrations.AlterField(
            model_name='ordencorte',
            name='tipoHuerta',
            field=models.CharField(choices=[('HSS', 'Aguacate Hass'), ('MDZ', 'Aguacate Mendez'), ('CLL', 'Aguacate Criollo')], default='', max_length=3),
        ),
        migrations.AlterField(
            model_name='reportecorte',
            name='cajasCortadas',
            field=models.FloatField(blank=True),
        ),
        migrations.CreateModel(
            name='FrutaHuerta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcionFruta', models.CharField(blank=True, max_length=500)),
                ('precioFruta', models.FloatField(blank=True)),
                ('idHuerta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Agronomunnity.huerta')),
            ],
            options={
                'verbose_name': 'FrutaHuerta',
                'verbose_name_plural': 'FrutaHuertas',
                'db_table': 'frutahuerta',
                'ordering': ['id'],
            },
        ),
    ]